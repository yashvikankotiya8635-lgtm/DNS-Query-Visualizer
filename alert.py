import pandas as pd

# Read CSV safely
encodings = ["utf-8", "latin1", "cp1252"]
df = None

for enc in encodings:
    try:
        df = pd.read_csv(
            "dns_log.csv",
            encoding=enc,
            on_bad_lines="skip"
        )
        print(f"CSV loaded using {enc}")
        break
    except:
        pass

if df is None:
    print("Unable to read dns_log.csv")
    exit()

# Check Domain column
if "Domain" not in df.columns:
    print("Domain column not found!")
    exit()

# Count domains
counts = df["Domain"].value_counts()

print("\n===== Suspicious DNS Activity =====\n")

found = False

# Detect repeated domains
for domain, count in counts.items():

    if count >= 5:

        print(f"ALERT: {domain} -> {count} requests")

        found = True

if not found:
    print("No suspicious activity detected")
