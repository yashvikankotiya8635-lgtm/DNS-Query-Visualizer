# Import required libraries
from flask import Flask, render_template, send_file
import pandas as pd
import os

# Create Flask app
app = Flask(__name__)


# HOME ROUTE
@app.route("/")
def home():

    # CSV file path
    file_path = "dns_log.csv"

    # Check file exists or not
    if not os.path.exists(file_path):

        return render_template(
            "index.html",
            tables="<h3>No data found. Run dns_sniffer.py first.</h3>",
            total_queries=0,
            unique_domains=0,
            countries=0
        )

    # Read CSV safely
    try:

        data = pd.read_csv(file_path)

    except:

        return render_template(
            "index.html",
            tables="<h3>Error reading CSV file.</h3>",
            total_queries=0,
            unique_domains=0,
            countries=0
        )

    # Check empty CSV
    if data.empty:

        return render_template(
            "index.html",
            tables="<h3>No DNS data captured yet.</h3>",
            total_queries=0,
            unique_domains=0,
            countries=0
        )

    # Last 20 rows
    recent = data.tail(20)

    # Statistics
    total_queries = len(data)

    unique_domains = data["Domain"].nunique()

    countries = data["Country"].nunique()

    # Send data to HTML page
    return render_template(

        "index.html",

        tables=recent.to_html(index=False),

        total_queries=total_queries,

        unique_domains=unique_domains,

        countries=countries
    )


# MAP ROUTE
@app.route("/map")
def open_map():

    # Open generated map file
    return send_file("dns_map.html")


# GRAPH ROUTE
@app.route("/graph")
def open_graph():

    # Open generated graph image
    return send_file("top_domains.png")


# Run Flask server
if __name__ == "__main__":

    app.run(debug=True)