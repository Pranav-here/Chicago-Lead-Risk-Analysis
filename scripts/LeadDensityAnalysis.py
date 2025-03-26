import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as ctx
import folium
from folium.plugins import HeatMap
from scipy.stats import gaussian_kde

# Load datasets
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_', regex=False)
    return df

service_lines = clean_column_names(pd.read_csv('data/service_lines_with_lat_lon.csv'))
census_data = clean_column_names(pd.read_csv('data/property_service_line_census.csv'))

# Rename and merge datasets
service_lines = service_lines.rename(columns={'longitude': 'lon', 'latitude': 'lat'})
census_data = census_data.rename(columns={'longitude': 'census_lon', 'latitude': 'census_lat'})

merged = pd.merge(service_lines, census_data, on='address', how='inner', suffixes=('_service', '_census'))
merged['longitude'] = merged['lon']
merged['latitude'] = merged['lat']

# Ensure required columns exist
required_columns = {'public_service_line_material_service', 'private_service_line_material_service', 'longitude', 'latitude'}
missing = required_columns - set(merged.columns)
if missing:
    raise ValueError(f"Missing critical columns: {missing}")

# Compute Kernel Density Estimation (KDE)
xy = np.vstack([merged['longitude'], merged['latitude']])
density = gaussian_kde(xy)(xy)
merged['density'] = density

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(merged, geometry=gpd.points_from_xy(merged.longitude, merged.latitude), crs='EPSG:4326').to_crs(epsg=3857)

# Static KDE heatmap with seaborn
plt.figure(figsize=(10, 8))
sns.kdeplot(x=merged['longitude'], y=merged['latitude'], fill=True, cmap='Reds', levels=50)
plt.scatter(merged['longitude'], merged['latitude'], c='black', s=1, alpha=0.5)
plt.title('Lead Service Line Density in Chicago')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('lead_density_heatmap.png', dpi=300)
plt.show()

# Interactive Heatmap with Folium
m = folium.Map(location=[41.8781, -87.6298], zoom_start=11, tiles='cartodbpositron')
heat_data = list(zip(merged['latitude'], merged['longitude'], merged['density']))
HeatMap(heat_data, radius=15).add_to(m)
m.save('interactive_lead_density_map.html')

print("Maps successfully generated: lead_density_heatmap.png & interactive_lead_density_map.html")
