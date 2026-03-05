import pandas as pd
import numpy as np
import json
from datetime import datetime

INPUT_FILE = "data/processed/cleaned_transactions.csv"
OUTPUT_FILE = "data/processed/customer_features.csv"
INFO_FILE = "data/processed/feature_info.json"

print("Loading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("Dataset loaded.")

# -----------------------------
# RFM Features
# -----------------------------

snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("Customer ID").agg({
    "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
    "Invoice": "nunique",
    "TotalPrice": "sum"
})

rfm.columns = ["Recency", "Frequency", "Monetary"]

# -----------------------------
# Avg Order Value
# -----------------------------

avg_order_value = df.groupby("Customer ID")["TotalPrice"].mean()

# -----------------------------
# Unique Products
# -----------------------------

unique_products = df.groupby("Customer ID")["StockCode"].nunique()

# -----------------------------
# Total Items Purchased
# -----------------------------

total_items = df.groupby("Customer ID")["Quantity"].sum()

# -----------------------------
# Avg Days Between Purchases
# -----------------------------

purchase_dates = df.groupby("Customer ID")["InvoiceDate"].apply(lambda x: x.sort_values().diff().dt.days.mean())

# -----------------------------
# Basket Size
# -----------------------------

basket_size = df.groupby(["Customer ID", "Invoice"])["Quantity"].sum().groupby("Customer ID").mean()

# -----------------------------
# Preferred Day
# -----------------------------

df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()

preferred_day = df.groupby("Customer ID")["DayOfWeek"].agg(lambda x: x.value_counts().index[0])

# -----------------------------
# Preferred Hour
# -----------------------------

df["Hour"] = df["InvoiceDate"].dt.hour

preferred_hour = df.groupby("Customer ID")["Hour"].agg(lambda x: x.value_counts().index[0])

# -----------------------------
# Country Diversity
# -----------------------------

country_diversity = df.groupby("Customer ID")["Country"].nunique()

# -----------------------------
# Customer Lifetime
# -----------------------------

customer_lifetime = df.groupby("Customer ID")["InvoiceDate"].agg(lambda x: (x.max() - x.min()).days)

# -----------------------------
# Purchase Velocity
# -----------------------------

purchase_velocity = rfm["Frequency"] / (customer_lifetime + 1)

# -----------------------------
# Purchases last 30/60/90 days
# -----------------------------

last_date = df["InvoiceDate"].max()

p30 = df[df["InvoiceDate"] >= last_date - pd.Timedelta(days=30)].groupby("Customer ID")["Invoice"].nunique()
p60 = df[df["InvoiceDate"] >= last_date - pd.Timedelta(days=60)].groupby("Customer ID")["Invoice"].nunique()
p90 = df[df["InvoiceDate"] >= last_date - pd.Timedelta(days=90)].groupby("Customer ID")["Invoice"].nunique()

# -----------------------------
# Product Diversity
# -----------------------------

product_diversity = unique_products

# -----------------------------
# Price Preferences
# -----------------------------

avg_price = df.groupby("Customer ID")["Price"].mean()
std_price = df.groupby("Customer ID")["Price"].std()

# -----------------------------
# Combine All Features
# -----------------------------

features = pd.DataFrame(index=rfm.index)

features["Recency"] = rfm["Recency"]
features["Frequency"] = rfm["Frequency"]
features["Monetary"] = rfm["Monetary"]
features["AvgOrderValue"] = avg_order_value
features["UniqueProducts"] = unique_products
features["TotalItems"] = total_items
features["AvgDaysBetweenPurchases"] = purchase_dates
features["BasketSize"] = basket_size
features["PreferredDay"] = preferred_day
features["PreferredHour"] = preferred_hour
features["CountryDiversity"] = country_diversity
features["CustomerLifetimeDays"] = customer_lifetime
features["PurchaseVelocity"] = purchase_velocity
features["Purchases_Last30Days"] = p30
features["Purchases_Last60Days"] = p60
features["Purchases_Last90Days"] = p90
features["ProductDiversityScore"] = product_diversity
features["AvgPricePreference"] = avg_price
features["StdPricePreference"] = std_price

features = features.fillna(0)

# -----------------------------
# RFM Scoring
# -----------------------------

features["R_Score"] = pd.qcut(features["Recency"], 4, labels=[4,3,2,1])
features["F_Score"] = pd.qcut(features["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
features["M_Score"] = pd.qcut(features["Monetary"], 4, labels=[1,2,3,4])

features["RFM_Score"] = features["R_Score"].astype(str) + features["F_Score"].astype(str) + features["M_Score"].astype(str)

# -----------------------------
# Customer Segmentation
# -----------------------------

features["CustomerSegment"] = "Regular"

features.loc[(features["R_Score"] == 4) & (features["F_Score"] == 4), "CustomerSegment"] = "Champions"
features.loc[(features["R_Score"] == 3) & (features["F_Score"] >= 3), "CustomerSegment"] = "Loyal"
features.loc[(features["R_Score"] <= 2) & (features["F_Score"] <= 2), "CustomerSegment"] = "At Risk"

# -----------------------------
# Save Features
# -----------------------------

features.to_csv(OUTPUT_FILE)

print("Customer features saved.")

# -----------------------------
# Feature Info JSON
# -----------------------------

info = {
    "customers": int(len(features)),
    "features": int(features.shape[1]),
    "generated_at": str(datetime.now())
}

with open(INFO_FILE, "w") as f:
    json.dump(info, f, indent=4)

print("Feature info saved.")
print("Feature engineering completed.")