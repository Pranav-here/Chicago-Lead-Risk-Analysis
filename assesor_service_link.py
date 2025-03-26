import folium
import pandas as pd

# Load data and clean NaN coordinates
df = pd.read_csv("data\service_lines_with_geocodes.csv")
df = df.dropna(subset=['latitude', 'longitude'])  # Remove rows with missing coordinates

# Check cleaned data
print(f"Plotting {len(df)} valid addresses")

# Create map
chicago = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

for idx, row in df.iterrows():
    color = 'red' if row['Public Service Line Material'] == 'LEAD' else 'blue'
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Address: {row['Address']}<br>Public Line: {row['Public Service Line Material']}",
        icon=folium.Icon(color=color)
    ).add_to(chicago)

chicago.save("service_line_map.html")