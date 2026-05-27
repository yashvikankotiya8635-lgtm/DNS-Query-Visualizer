# Import required libraries
from scapy.all import sniff, DNS, DNSQR
import requests
import csv
from datetime import datetime
import os
import time


# Ignore unnecessary domains
ignore_domains = [
    "microsoft", "bing", "office", "windows", "vscode", "msedge",
    "msn", "live", "skype", "clarity", "icloud", "trafficmanager",
    "whatsapp", "apple", "outlook", "signalr", "iris", "akadns",
    "digicert", "gstatic", "ip-api", "msftconnecttest", "ecs", "setup"
]


# Store already processed IPs
seen_ips = set()


# Check private IP
def is_private(ip):
    try:
        parts = ip.split(".")
        return (
            ip.startswith("192.168.") or
            ip.startswith("10.") or
            (ip.startswith("172.") and 16 <= int(parts[1]) <= 31)
        )
    except:
        return False


# GeoIP function (FIXED)
def get_location(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=3)
        data = response.json()

        # IMPORTANT CHECK
        if data.get("status") != "success":
            return None

        return data

    except:
        print("API Error Occurred")
        return None


# Create CSV
def create_csv():
    if not os.path.exists("dns_log.csv"):
        with open("dns_log.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp",
                "Domain",
                "IP Address",
                "Country",
                "City",
                "Latitude",
                "Longitude"
            ])


# Save to CSV
def save_to_csv(domain, ip, country, city, lat, lon):
    with open("dns_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now(),
            domain,
            ip,
            country,
            city,
            lat,
            lon
        ])


# DNS packet handler
def detect_dns(packet):

    if packet.haslayer(DNS):

        if packet[DNS].qr == 1:

            if packet[DNS].ancount > 0:

                try:
                    domain = packet[DNSQR].qname.decode().strip().lower()
                except:
                    return

                # ignore unwanted domains
                for word in ignore_domains:
                    if word in domain:
                        return

                print("\n==========================")
                print("Domain:", domain)

                answers = packet[DNS].an

                for i in range(packet[DNS].ancount):

                    answer = answers[i]

                    # IPv4
                    if answer.type == 1:

                        ip = str(answer.rdata)

                        if ip in seen_ips:
                            continue

                        seen_ips.add(ip)

                        print("IPv4:", ip)

                        if is_private(ip):
                            print("Private IP Skipped")
                            continue

                        location = get_location(ip)

                        if location:
                            
                            print(location)
                            country = location.get("country", "Unknown")
                            city = location.get("city", "Unknown")
                            lat = location.get("lat")
                            lon = location.get("lon")

                            # FINAL SAFETY CHECK (NO NaN)
                            if lat is None or lon is None:
                                print("Geo data missing, skipped")
                                continue

                            print("Country:", country)
                            print("City:", city)
                            print("Latitude:", lat)
                            print("Longitude:", lon)

                            save_to_csv(domain, ip, country, city, lat, lon)

                            print("Saved to CSV")

                            time.sleep(0.2)

                    # IPv6
                    elif answer.type == 28:

                        ip = str(answer.rdata)

                        if ip in seen_ips:
                            continue

                        seen_ips.add(ip)

                        print("IPv6:", ip)


# Initialize CSV
create_csv()


# Start sniffing
sniff(
    filter="udp port 53",
    prn=detect_dns,
    store=0
)