# Import libraries
import pandas as pd
import matplotlib.pyplot as plt

# Try different encodings
encodings = ["utf-8", "latin1", "cp1252"]

df = None

for enc in encodings:
    try:
        df = pd.read_csv(
            "dns_log.csv",
            encoding=enc,
            on_bad_lines="skip"
        )
        print(f"CSV loaded successfully using {enc} encoding")
        break
    except Exception:
        pass

# If CSV cannot be loaded
if df is None:
    print("Unable to read dns_log.csv")
    exit()

# Check if file is empty
if df.empty:
    print("No data found in dns_log.csv")
    exit()

# Show column names
print("Columns found:", df.columns.tolist())

# Check Domain column exists
if "Domain" not in df.columns:
    print("Domain column not found!")
    exit()

# Remove empty values
df = df.dropna(subset=["Domain"])

# Count top domains
top_domains = df["Domain"].value_counts().head(10)

# Check if data exists
if top_domains.empty:
    print("No domain data available")
    exit()

# Create graph
plt.figure(figsize=(12, 6))
top_domains.plot(kind="bar")

plt.title("Top 10 DNS Queried Domains")
plt.xlabel("Domain Name")
plt.ylabel("Number of Queries")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save graph
plt.savefig("static/top_domains.png")

print("Graph generated successfully!")
print("File saved as: top_domains.png")

# Display graph
plt.show()
