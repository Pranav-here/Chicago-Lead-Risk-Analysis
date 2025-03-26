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

# Clean merged neighborhood data
service_lines_with_neighborhood.drop_duplicates(inplace=True)
service_lines_with_neighborhood.dropna(subset=['longitude', 'latitude', 'nbhd'], inplace=True)

# # Optional: Rename 'nbhd' to 'neighborhood' for clarity
# service_lines_with_neighborhood.rename(columns={'nbhd': 'neighborhood'}, inplace=True)

# Save the final dataset
service_lines_with_neighborhood.to_csv('data\\service_lines_with_neighborhood.csv', index=False)

# Summary
print(f"Final dataset contains {len(service_lines_with_neighborhood)} entries.")
print(service_lines_with_neighborhood.head())
