import pandas as pd

# Read CSV
df = pd.read_csv("dns_log.csv")

# Count domains
counts = df["Domain"].value_counts()

print("\n===== Suspicious DNS Activity =====\n")

found = False

# Detect high repeated domains
for domain, count in counts.items():

    if count >= 5:

        print(f"ALERT: {domain} -> {count} requests")

        found = True

if not found:
    print("No suspicious activity detected")