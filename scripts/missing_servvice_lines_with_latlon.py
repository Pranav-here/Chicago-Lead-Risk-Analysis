import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from time import sleep

# Load the datasets
service_lines_material = pd.read_csv('data/T096318_Responsive_Document.csv')
service_lines_with_lat_lon = pd.read_csv('data/service_lines_with_lat_lon.csv')

# Find rows that are in service_lines_material but not in service_lines_with_lat_lon
missing_rows = service_lines_material[~service_lines_material['Address'].isin(service_lines_with_lat_lon['Address'])]

# Geocode missing addresses with rate limiting
geolocator = Nominatim(user_agent="geoapiExercises")

def get_lat_lon(address):
    retries = 3
    for _ in range(retries):
        try:
            location = geolocator.geocode(address + ", Chicago, IL", timeout=10)
            if location:
                return pd.Series([location.latitude, location.longitude])
        except GeocoderTimedOut:
            print(f"Timeout for {address}, retrying...")
            sleep(2)
        except Exception as e:
            print(f"Error geocoding {address}: {e}")
            break
    return pd.Series([None, None])

# Apply geocoding with a delay to avoid rate limits
missing_rows[['latitude', 'longitude']] = missing_rows['Address'].apply(lambda x: get_lat_lon(x))
sleep(1)  # Rate limiting

# Save to a new CSV file
missing_rows.to_csv('data/missing_service_lines_with_lat_lon.csv', index=False)

print("Geocoded addresses saved to 'data/missing_service_lines_with_lat_lon.csv'")
