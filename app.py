from flask import Flask, render_template, send_file, jsonify
import pandas as pd
import os
import math
from collections import Counter

app = Flask(__name__)

CSV_FILE = "dns_log.csv"


# ================================
# CALCULATE ENTROPY
# ================================
def calculate_entropy(domain):
    counts = Counter(domain)
    length = len(domain)

    if length == 0:
        return 0

    return -sum((c / length) * math.log2(c / length) for c in counts.values())


# ================================
# DETECT ATTACK TYPE
# ================================
def detect_attack_type(domain):
    domain = str(domain).lower()

    suspicious_keywords = [
        "login", "verify", "secure",
        "bank", "paypal", "amazon"
    ]

    for word in suspicious_keywords:
        if word in domain:
            return "PHISHING"

    entropy = calculate_entropy(domain)

    if entropy > 4.2:
        return "MALWARE"

    return "SAFE"


# ================================
# DOT COLOR
# ================================
def get_dot_color(attack_type):
    if attack_type == "PHISHING":
        return "red"
    elif attack_type == "MALWARE":
        return "orange"
    else:
        return "green"


# ================================
# HOME PAGE
# ================================
@app.route("/")
def home():
    return render_template("index.html")


# ================================
# FOLIUM MAP PAGE
# ================================
@app.route("/map")
def open_map():
    if os.path.exists("dns_map.html"):
        return send_file("dns_map.html")
    return "dns_map.html not found. Please run map.py first."


# ================================
# GRAPH PAGE
# ================================
@app.route("/graph")
def open_graph():
    graph_path = "static/top_domains.png"

    if os.path.exists(graph_path):
        return send_file(graph_path)

    return "top_domains.png not found. Please run graph.py first."


# ================================
# GET DNS QUERIES FOR DASHBOARD MAP
# ================================
@app.route("/get-queries")
def get_queries():
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify([])

        data = pd.read_csv(CSV_FILE)

        if data.empty:
            return jsonify([])

        queries = []

        for _, row in data.tail(50).iterrows():

            lat = row.get("Latitude")
            lon = row.get("Longitude")

            if pd.isna(lat) or pd.isna(lon):
                continue

            domain = str(row.get("Domain", "Unknown"))
            attack_type = detect_attack_type(domain)

            queries.append({
                "domain": domain,
                "ip": str(row.get("IP Address", "Unknown")),
                "country": str(row.get("Country", "Unknown")),
                "city": str(row.get("City", "Unknown")),
                "lat": float(lat),
                "lon": float(lon),
                "attack_type": attack_type,
                "color": get_dot_color(attack_type)
            })

        return jsonify(queries)

    except Exception as e:
        print("Error in /get-queries:", e)
        return jsonify([])


# ================================
# GET ALERTS
# ================================
@app.route("/get-alerts")
def get_alerts():
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify([])

        data = pd.read_csv(CSV_FILE)

        alerts = []

        for _, row in data.tail(50).iterrows():

            domain = str(row.get("Domain", "Unknown"))
            attack = detect_attack_type(domain)

            if attack != "SAFE":
                alerts.append({
                    "domain": domain,
                    "attack": attack,
                    "country": str(row.get("Country", "Unknown")),
                    "time": str(row.get("Timestamp", "Unknown")),
                    "color": get_dot_color(attack)
                })

        return jsonify(alerts)

    except Exception as e:
        print("Error in /get-alerts:", e)
        return jsonify([])


# ================================
# GET DASHBOARD STATS
# ================================
@app.route("/get-stats")
def get_stats():
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify({
                "total_queries": 0,
                "phishing_detected": 0,
                "malware_detected": 0,
                "safe_queries": 0,
                "countries_involved": []
            })

        data = pd.read_csv(CSV_FILE)

        phishing = 0
        malware = 0
        safe = 0
        countries = set()

        for _, row in data.iterrows():

            country = str(row.get("Country", "Unknown"))
            if country != "nan":
                countries.add(country)

            domain = str(row.get("Domain", "Unknown"))
            attack = detect_attack_type(domain)

            if attack == "PHISHING":
                phishing += 1
            elif attack == "MALWARE":
                malware += 1
            else:
                safe += 1

        return jsonify({
            "total_queries": len(data),
            "phishing_detected": phishing,
            "malware_detected": malware,
            "safe_queries": safe,
            "countries_involved": list(countries)
        })

    except Exception as e:
        print("Error in /get-stats:", e)

        return jsonify({
            "total_queries": 0,
            "phishing_detected": 0,
            "malware_detected": 0,
            "safe_queries": 0,
            "countries_involved": []
        })


# ================================
# RUN FLASK APP
# ================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
