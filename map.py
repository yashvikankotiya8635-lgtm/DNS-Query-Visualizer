import pandas as pd
import folium
import os

file_path = "dns_log.csv"

if not os.path.exists(file_path):
    print("dns_log.csv file not found.")
    exit()

df = pd.read_csv(file_path)

dns_map = folium.Map(
    location=[20, 0],
    zoom_start=2
)

for index, row in df.iterrows():
    lat = row["Latitude"]
    lon = row["Longitude"]

    if pd.isna(lat) or pd.isna(lon):
        continue

    domain = row["Domain"]
    ip = row["IP Address"]
    country = row["Country"]
    city = row["City"]

    color = "blue"

    if country == "India":
        color = "green"
    elif country == "United States":
        color = "red"
    elif country == "Germany":
        color = "orange"
    elif country == "Canada":
        color = "purple"
    else:
        color = "blue"

    popup_text = f"""
    <b>Domain:</b> {domain}<br>
    <b>IP Address:</b> {ip}<br>
    <b>Country:</b> {country}<br>
    <b>City:</b> {city}
    """

    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        tooltip=domain,
        icon=folium.Icon(color=color)
    ).add_to(dns_map)

dns_map.save("dns_map.html")

print("Map generated successfully: dns_map.html")
