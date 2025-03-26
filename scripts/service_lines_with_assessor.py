# # Merge the assessor data to service lines based on address to map service line to assessor information
# import pandas as pd
#
# # Load assessor data (Assessor__Archived_05-11-2022__-_Property_Locations_20250304.csv)
# assessor_data = pd.read_csv('data\Assessor__Archived_05-11-2022__-_Property_Locations_20250304.csv')
#
# service_lines_with_geocodes = pd.read_csv('data\service_lines_with_geocodes.csv')
# service_lines_material = pd.read_csv('data\T096318_Responsive_Document.csv')
# merged_service_lines = pd.merge(service_lines_material, service_lines_with_geocodes[['Address', 'longitude', 'latitude']],
#                                 left_on='Address', right_on='Address', how='left')
#
# # Merge based on address to associate neighborhood
# service_lines_with_neighborhood = pd.merge(merged_service_lines, assessor_data[['property_address', 'nbhd']],
#                                             left_on='Address', right_on='property_address', how='left')
#
# service_lines_with_assessor = pd.merge(service_lines_with_neighborhood, assessor_data[['property_address', 'pin', 'longitude', 'latitude']],
#                                        left_on='Address', right_on='property_address', how='left')
#
# # Save or review the merged dataset
# service_lines_with_assessor.to_csv('data\service_lines_with_assessor.csv', index=False)
# print(service_lines_with_assessor.head())


import pandas as pd

# Load data
assessor_data = pd.read_csv('data\\Assessor__Archived_05-11-2022__-_Property_Locations_20250304.csv')
service_lines_with_geocodes = pd.read_csv('data\\service_lines_with_geocodes.csv')
service_lines_material = pd.read_csv('data\\T096318_Responsive_Document.csv')

# Merge geocodes with material data
merged_service_lines = pd.merge(service_lines_material,
                                service_lines_with_geocodes[['Address', 'longitude', 'latitude']],
                                left_on='Address', right_on='Address', how='left')

# Clean merged service lines data
merged_service_lines.drop_duplicates(inplace=True)
merged_service_lines.dropna(subset=['longitude', 'latitude'], inplace=True)

# Merge with assessor data to add neighborhood information
service_lines_with_neighborhood = pd.merge(merged_service_lines,
                                            assessor_data[['property_address', 'nbhd']],
                                            left_on='Address', right_on='property_address', how='left')

# Clean neighborhood data
service_lines_with_neighborhood.drop_duplicates(inplace=True)
service_lines_with_neighborhood.dropna(subset=['nbhd'], inplace=True)

# Merge with assessor data again to add PIN and coordinates
service_lines_with_assessor = pd.merge(service_lines_with_neighborhood,
                                       assessor_data[['property_address', 'pin', 'longitude', 'latitude']],
                                       left_on='Address', right_on='property_address', how='left')

# Clean final merged data
service_lines_with_assessor.drop_duplicates(inplace=True)
service_lines_with_assessor.dropna(inplace=True)

# Save the cleaned dataset
service_lines_with_assessor.to_csv('data\\service_lines_with_assessor.csv', index=False)

# Summary
print(f"Final dataset contains {len(service_lines_with_assessor)} entries.")
print(service_lines_with_assessor.head())
