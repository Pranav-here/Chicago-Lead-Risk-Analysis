import folium

# Merge the assessor data to service lines based on address to map service line to assessor information
import pandas as pd

# Load assessor data (Assessor__Archived_05-11-2022__-_Property_Locations_20250304.csv)
assessor_data = pd.read_csv('data\Assessor__Archived_05-11-2022__-_Property_Locations_20250304.csv')

service_lines_with_geocodes = pd.read_csv('data\service_lines_with_geocodes.csv')
service_lines_material = pd.read_csv('data\T096318_Responsive_Document.csv')
merged_service_lines = pd.merge(service_lines_material, service_lines_with_geocodes[['Address', 'longitude', 'latitude']],
                                left_on='Address', right_on='Address', how='left')

# Merge based on address to associate neighborhood
service_lines_with_neighborhood = pd.merge(merged_service_lines, assessor_data[['property_address', 'nbhd']],
                                            left_on='Address', right_on='property_address', how='left')

service_lines_with_assessor = pd.merge(service_lines_with_neighborhood, assessor_data[['property_address', 'pin', 'longitude', 'latitude']],
                                       left_on='Address', right_on='property_address', how='left')

# Merge based on address to associate latitude and longitude
service_lines_with_lat_lon = pd.merge(service_lines_material, service_lines_with_geocodes[['Address', 'longitude', 'latitude']],
                                left_on='Address', right_on='Address', how='left')


# Initialize map centered at an average location
map_center = [41.8781, -87.6298]  # Example: Chicago's latitude and longitude
m = folium.Map(location=map_center, zoom_start=12)

# Add each service line location as a marker on the map
for _, row in service_lines_with_lat_lon.iterrows():
    folium.Marker([row['latitude'], row['longitude']],
                  popup=f"Address: {row['Address']}\nMaterial: {row['Private Service Line Material']}").add_to(m)

# Save map to HTML
m.save('service_lines_map.html')
