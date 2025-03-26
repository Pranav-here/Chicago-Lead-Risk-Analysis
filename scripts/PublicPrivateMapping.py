import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx

def clean_column_names(df):
    """Standardize column names across datasets"""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_', regex=False)
    return df

# Load data with coordinate validation
service_lines = clean_column_names(pd.read_csv('data/service_lines_with_lat_lon.csv'))
census_data = clean_column_names(pd.read_csv('data/property_service_line_census.csv'))

# Explicitly rename coordinate columns before merging
service_lines = service_lines.rename(columns={
    'longitude': 'lon',
    'latitude': 'lat'
})

census_data = census_data.rename(columns={
    'longitude': 'census_lon',
    'latitude': 'census_lat'
})

# Merge on address with conflict resolution
merged = pd.merge(
    service_lines,
    census_data,
    on='address',
    how='inner',
    suffixes=('_service', '_census')
)

# Use service line coordinates as primary
merged['longitude'] = merged['lon']
merged['latitude'] = merged['lat']

# Verify critical columns
required_columns = {
    'public_service_line_material_service',
    'private_service_line_material_service',
    'longitude',
    'latitude'
}

print("Actual columns:", merged.columns.tolist())
missing = required_columns - set(merged.columns)
if missing:
    raise ValueError(f"Missing critical columns: {missing}\nExisting columns: {merged.columns.tolist()}")

# Create risk score calculation with verified columns
def calculate_risk(row):
    risk = 0
    public_line = row['public_service_line_material_service']
    private_line = row['private_service_line_material_service']

    if public_line == 'LEAD': risk += 0.3  # Public now blue
    if private_line == 'LEAD': risk += 0.7  # Private now red
    return risk

merged['risk_score'] = merged.apply(calculate_risk, axis=1)

# Create GeoDataFrame with coordinate validation
gdf = gpd.GeoDataFrame(
    merged,
    geometry=gpd.points_from_xy(
        merged.longitude.astype(float),
        merged.latitude.astype(float),
        crs="EPSG:4326"
    )
).to_crs(epsg=3857)

# Visualization with error handling
try:
    fig, ax = plt.subplots(figsize=(18, 12))

    gdf.plot(column='risk_score', ax=ax, markersize=10,
             legend=True, cmap='coolwarm', alpha=0.7,  # Updated colormap
             legend_kwds={'label': "Lead Exposure Risk Score"})

    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    ax.set_title('Chicago Lead Exposure Risk Map\nPublic Service Lines & Risk Scoring', fontsize=16)
    ax.set_axis_off()

    plt.savefig('lead_risk_map.png', dpi=300, bbox_inches='tight')
    print("Visualization successfully created: lead_risk_map_pub_pvt.png")

except Exception as e:
    print(f"Visualization failed: {str(e)}")
    raise

import folium
from folium.plugins import MarkerCluster
from branca.colormap import LinearColormap
import pandas as pd

# Load and prepare data (using your working merged dataframe)
merged = pd.read_csv('data/merged_data_for_maps.csv')  # Save your merged data if not already

# Create Chicago base map
m = folium.Map(location=[41.8781, -87.6298],
               zoom_start=11,
               tiles='cartodbpositron')

# Create risk score color scale
colormap = LinearColormap(
    colors=['#0000ff', '#ffff00', '#ff0000'],  # Blue-Yellow-Red (Public=Blue, Private=Red)
    vmin=merged['risk_score'].min(),
    vmax=merged['risk_score'].max()
)

# Add marker cluster for performance
marker_cluster = MarkerCluster(
    name="Lead Risk Properties",
    overlay=True,
    control=True
).add_to(m)

# Add individual markers with tooltips
for idx, row in merged.iterrows():
    popup_html = f"""
    <b>Address:</b> {row['address']}<br>
    <b>Public Line:</b> {row['public_service_line_material_service']}<br>
    <b>Private Line:</b> {row['private_service_line_material_service']}<br>
    <b>Risk Score:</b> {row['risk_score']:.2f}<hr>
    <b>Census Tract:</b> {row['tract_geoid']}<br>
    <b>Median Income:</b> ${row['tract_midincome']:,.0f}
    """

    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color=colormap(row['risk_score']),
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"Risk: {row['risk_score']:.2f}",
        weight=1
    ).add_to(marker_cluster)

# Add layer control and color scale
colormap.add_to(m)
folium.LayerControl().add_to(m)

# Save interactive map
m.save('interactive_lead_risk_map.html')