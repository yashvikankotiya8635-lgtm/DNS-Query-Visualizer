import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dns_log.csv")
print(df.columns)

# Read CSV
df = pd.read_csv("dns_log.csv")

# Top 5 domains
top_domains = df["Domain"].value_counts().head(5)

# Create graph
plt.figure(figsize=(8,5))

top_domains.plot(kind="bar")

plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.title("Top DNS Domains")
plt.xlabel("Domain")
plt.ylabel("Query Count")

# Save graph
plt.savefig("top_domains.png")

print("Graph Created Successfully")