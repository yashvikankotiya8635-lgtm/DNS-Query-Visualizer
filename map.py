import pandas as pd
import folium

# Read CSV
df = pd.read_csv("dns_log.csv")

# Create world map
dns_map = folium.Map(
    location=[20, 78],
    zoom_start=2
)

# Add markers
for i in range(len(df)):

    lat = df.loc[i, "Latitude"]
    lon = df.loc[i, "Longitude"]
    domain = df.loc[i, "Domain"]

    # Ignore unnecessary domains
    ignore = [
        "bing",
        "microsoft",
        "icloud",
        "msn",
        "googlevideo",
        "cloudfront",
        "gstatic",
        "akadns"
    ]

    skip = False

    for word in ignore:
        if word in str(domain).lower():
            skip = True

    if skip:
        continue

    # Ignore NaN
    if pd.notnull(lat) and pd.notnull(lon):

        folium.Marker(
            [lat, lon],
            popup=domain
        ).add_to(dns_map)

# Save map
dns_map.save("dns_map.html")

print("Map Created Successfully")