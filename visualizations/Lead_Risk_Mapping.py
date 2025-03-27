import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import folium
from folium.plugins import MarkerCluster, Fullscreen
from branca.colormap import LinearColormap

def clean_column_names(df):
    """Standardize column names across datasets"""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_', regex=False)
    return df

# Load data
service_lines = clean_column_names(pd.read_csv('data/service_lines_with_lat_lon.csv'))
service_lines = service_lines.drop_duplicates(subset=['address'])
service_lines.dropna(inplace=True)  # Ensure no missing values

census_data = clean_column_names(pd.read_csv('data/property_service_line_census.csv'))
census_data = census_data.drop_duplicates(subset=['address'])
census_data.dropna(inplace=True)


# Ensure longitude and latitude are float
service_lines[['longitude', 'latitude']] = service_lines[['longitude', 'latitude']].astype(float)
census_data[['longitude', 'latitude']] = census_data[['longitude', 'latitude']].astype(float)

# Rename for clarity
service_lines = service_lines.rename(columns={'longitude': 'lon', 'latitude': 'lat'})
census_data = census_data.rename(columns={'longitude': 'census_lon', 'latitude': 'census_lat'})

# Merge datasets
merged = pd.merge(service_lines, census_data, on='address', how='inner', suffixes=('_service', '_census'), validate='one_to_one')
merged['longitude'] = merged['lon']
merged['latitude'] = merged['lat']

# Ensure required columns exist
required_columns = {'public_service_line_material_service', 'private_service_line_material_service', 'longitude', 'latitude'}
missing = required_columns - set(merged.columns)
if missing:
    raise ValueError(f"Missing critical columns: {missing}")

# Risk Score Calculation
def calculate_risk(row):
    risk = 0
    if row['public_service_line_material_service'] == 'LEAD':
        risk += 0.7  # Public pipes more risky
    if row['private_service_line_material_service'] == 'LEAD':
        risk += 0.3  # Private pipes less risky
    return risk

merged['risk_score'] = merged.apply(calculate_risk, axis=1)

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(merged, geometry=gpd.points_from_xy(merged.longitude, merged.latitude, crs="EPSG:4326")).to_crs(epsg=3857)

# Matplotlib Visualization
fig, ax = plt.subplots(figsize=(18, 12))
gdf.plot(column='risk_score', ax=ax, markersize=merged['risk_score'] * 50, legend=True, cmap='coolwarm', alpha=0.7, legend_kwds={'label': "Lead Exposure Risk Score"})
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
ax.set_title('Chicago Lead Exposure Risk Map', fontsize=16)
ax.set_axis_off()
plt.savefig('lead_risk_map_2.png', dpi=300, bbox_inches='tight')

# Interactive Map
m = folium.Map(location=[41.8781, -87.6298], zoom_start=11, tiles='cartodbpositron')
colormap = LinearColormap(colors=['#0000ff', '#ffff00', '#ff0000'], vmin=merged['risk_score'].min(), vmax=merged['risk_score'].max())
marker_cluster = MarkerCluster(name="Lead Risk Properties", overlay=True, control=True).add_to(m)

for idx, row in merged.iterrows():
    popup_html = f"""
    <b>Address:</b> {row['address']}<br>
    <b>Public Line:</b> {row['public_service_line_material_service']}<br>
    <b>Private Line:</b> {row['private_service_line_material_service']}<br>
    <b>Risk Score:</b> {row['risk_score']:.2f}
    """
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=max(3, row['risk_score'] * 10),
        color=colormap(row['risk_score']),
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"Risk: {row['risk_score']:.2f}",
    ).add_to(marker_cluster)

colormap.add_to(m)
folium.LayerControl().add_to(m)
Fullscreen(position='topright').add_to(m)
m.save('interactive_lead_risk_map_2.html')
