import pandas as pd

# Load the datasets
service_lines_material = pd.read_csv('data/T096318_Responsive_Document.csv')
service_lines_with_lat_lon = pd.read_csv('data/service_lines_with_lat_lon.csv')

# Find rows that are in service_lines_material but not in service_lines_with_lat_lon
missing_rows = service_lines_material[~service_lines_material['Address'].isin(service_lines_with_lat_lon['Address'])]

# Save to a new CSV file
missing_rows.to_csv('data/missing_service_lines.csv', index=False)

print("Filtered rows saved to 'data/missing_service_lines.csv'")