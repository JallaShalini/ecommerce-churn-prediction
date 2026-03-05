import pandas as pd
import json
from datetime import datetime

# -----------------------------
# File paths
# -----------------------------

INPUT_FILE = "data/raw/online_retail.csv"
OUTPUT_FILE = "data/processed/cleaned_transactions.csv"
STATS_FILE = "data/processed/cleaning_statistics.json"

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

initial_rows = len(df)

print("Initial rows:", initial_rows)

# -----------------------------
# Convert datatypes
# -----------------------------

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# -----------------------------
# Remove missing CustomerID
# -----------------------------

df = df.dropna(subset=["Customer ID"])

after_customer_filter = len(df)

# -----------------------------
# Remove cancellations
# (Invoices starting with C)
# -----------------------------

df = df[~df["Invoice"].astype(str).str.startswith("C")]

after_cancellations = len(df)

# -----------------------------
# Remove negative quantities
# -----------------------------

df = df[df["Quantity"] > 0]

after_quantity = len(df)

# -----------------------------
# Remove zero prices
# -----------------------------

df = df[df["Price"] > 0]

after_price = len(df)

# -----------------------------
# Remove missing descriptions
# -----------------------------

df = df.dropna(subset=["Description"])

after_description = len(df)

# -----------------------------
# Remove outliers using IQR
# -----------------------------

Q1 = df["Quantity"].quantile(0.25)
Q3 = df["Quantity"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

df = df[(df["Quantity"] >= lower) & (df["Quantity"] <= upper)]

after_outliers = len(df)

# -----------------------------
# Remove duplicates
# -----------------------------

df = df.drop_duplicates()

after_duplicates = len(df)

# -----------------------------
# Create derived columns
# -----------------------------

df["TotalPrice"] = df["Quantity"] * df["Price"]

df["InvoiceYear"] = df["InvoiceDate"].dt.year
df["InvoiceMonth"] = df["InvoiceDate"].dt.month
df["InvoiceDay"] = df["InvoiceDate"].dt.day

# -----------------------------
# Save cleaned dataset
# -----------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("Cleaned dataset saved.")

# -----------------------------
# Create statistics report
# -----------------------------

stats = {
    "initial_rows": initial_rows,
    "after_customer_filter": after_customer_filter,
    "after_cancellations": after_cancellations,
    "after_quantity_filter": after_quantity,
    "after_price_filter": after_price,
    "after_description_filter": after_description,
    "after_outlier_removal": after_outliers,
    "after_duplicate_removal": after_duplicates,
    "final_rows": len(df),
    "retention_rate": round(len(df) / initial_rows * 100, 2),
    "generated_at": str(datetime.now())
}

with open(STATS_FILE, "w") as f:
    json.dump(stats, f, indent=4)

print("Cleaning statistics saved.")

print("Data cleaning completed successfully.")