import pandas as pd

# Load service line data with geocodes
service_lines_with_geocodes = pd.read_csv('data\service_lines_with_geocodes.csv')

# Load the service line material data (T096318_Responsive_Document.csv)
service_lines_material = pd.read_csv('data\T096318_Responsive_Document.csv')

# Merge based on address to associate latitude and longitude
merged_service_lines = pd.merge(service_lines_material, service_lines_with_geocodes[['Address', 'longitude', 'latitude']],
                                left_on='Address', right_on='Address', how='left')

merged_service_lines.drop_duplicates(inplace=True)
merged_service_lines.dropna(inplace=True)

# Save or review the merged dataset
merged_service_lines.to_csv('data\\service_lines_with_lat_lon.csv', index=False)
print(merged_service_lines.head())
