# import pandas as pd
# from geopy.geocoders import Nominatim
#
# # Load merged data
# df = pd.read_csv("data\\property_service_line_census.csv")
#
# # Drop duplicates and rows with missing coordinates
# df.drop_duplicates(inplace=True)
# df.dropna(subset=['latitude', 'longitude'], inplace=True)
#
# # Check for remaining missing coordinates
# missing_coords = df[df['latitude'].isna() | df['longitude'].isna()]
# print(f"Missing coordinates for {len(missing_coords)} addresses.")
#
# # Optionally, use a geocoding API for missing entries
# geolocator = Nominatim(user_agent="geo_services")
#
# # Save cleaned data
# df.to_csv("service_lines_with_geocodes.csv", index=False)
# print("Cleaned data saved successfully!")


import pandas as pd
from geopy.geocoders import Nominatim

# Load merged data
df = pd.read_csv("data\\property_service_line_census.csv")

# Drop duplicates and rows with missing coordinates
df.drop_duplicates(inplace=True)
df.dropna(subset=['latitude', 'longitude'], inplace=True)

# Check for remaining missing coordinates
missing_coords = df[df['latitude'].isna() | df['longitude'].isna()]
print(f"Missing coordinates for {len(missing_coords)} addresses.")

# Geocoding logic for missing coordinates
geolocator = Nominatim(user_agent="geo_services")

for index, row in missing_coords.iterrows():
    try:
        location = geolocator.geocode(row['Address'])
        if location:
            df.at[index, 'latitude'] = location.latitude
            df.at[index, 'longitude'] = location.longitude
    except Exception as e:
        print(f"Geocoding failed for address: {row['Address']} - {e}")

# Final cleaning step (drop any still-missing coordinates)
df.dropna(subset=['latitude', 'longitude'], inplace=True)

# Save cleaned data
df.to_csv("data\\service_lines_with_geocodes.csv", index=False)
print(f"Cleaned data saved successfully with {len(df)} entries.")
