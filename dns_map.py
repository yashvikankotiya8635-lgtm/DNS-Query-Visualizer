# Import libraries
import pandas as pd
import folium

# Read CSV file
df = pd.read_csv("dns_log.csv")

# Create world map
dns_map = folium.Map(
    location=[20, 0],
    zoom_start=2
)

# Loop through CSV rows
for index, row in df.iterrows():

    # Latitude & Longitude
    lat = row["Latitude"]
    lon = row["Longitude"]

    # Skip missing values
    if pd.isna(lat) or pd.isna(lon):
        continue

    # DNS information
    domain = row["Domain"]
    ip = row["IP Address"]
    country = row["Country"]
    city = row["City"]

    # Default color
    color = "blue"

    # Country colors
    if country == "India":
        color = "green"

    elif country == "United States":
        color = "red"

    elif country == "Germany":
        color = "orange"

    elif country == "Canada":
        color = "purple"

    elif country == "Japan":
        color = "pink"

    # Create Circle Marker
    folium.CircleMarker(

        location=[lat, lon],

        radius=8,

        popup=f"""
        Domain: {domain}<br>
        IP: {ip}<br>
        Country: {country}<br>
        City: {city}
        """,

        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8

    ).add_to(dns_map)

# Save HTML map
dns_map.save("dns_map.html")

print("DNS Map Created Successfully")