import pandas as pd
import json
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

INPUT_FILE = "data/processed/customer_features.csv"

print("Loading customer features...")

df = pd.read_csv(INPUT_FILE)

print("Dataset shape:", df.shape)

# -----------------------------
# Remove Customer ID
# -----------------------------

if "Customer ID" in df.columns:
    df = df.drop(columns=["Customer ID"])

# -----------------------------
# Encode Customer Segment
# -----------------------------

df["CustomerSegment"] = df["CustomerSegment"].astype("category").cat.codes
df["PreferredDay"] = df["PreferredDay"].astype("category").cat.codes
# -----------------------------
# Create Target Variable
# (Example churn definition)
# -----------------------------

df["Churn"] = (df["Recency"] > 90).astype(int)

# -----------------------------
# Split Features / Target
# -----------------------------

X = df.drop(columns=[
    "Churn",
    "Recency",

    "Frequency",
    "Monetary",

    "Purchases_Last30Days",
    "Purchases_Last60Days",
    "Purchases_Last90Days",

    "AvgDaysBetweenPurchases",
    "PurchaseVelocity",
    "CustomerLifetimeDays",

    "AvgOrderValue",
    "TotalItems",
    "UniqueProducts"
])
y = df["Churn"]

print("Feature shape:", X.shape)

# -----------------------------
# Train / Temp Split (70 / 30)
# -----------------------------

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.30,
    stratify=y,
    random_state=42
)

# -----------------------------
# Validation / Test Split (15 / 15)
# -----------------------------

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    stratify=y_temp,
    random_state=42
)

print("Train size:", X_train.shape)
print("Validation size:", X_val.shape)
print("Test size:", X_test.shape)

# -----------------------------
# Scale Features
# -----------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Convert back to DataFrame

X_train = pd.DataFrame(X_train_scaled, columns=X.columns)
X_val = pd.DataFrame(X_val_scaled, columns=X.columns)
X_test = pd.DataFrame(X_test_scaled, columns=X.columns)

# -----------------------------
# Save Datasets
# -----------------------------

X_train.to_csv("data/processed/X_train.csv", index=False)
X_val.to_csv("data/processed/X_val.csv", index=False)
X_test.to_csv("data/processed/X_test.csv", index=False)

y_train.to_csv("data/processed/y_train.csv", index=False)
y_val.to_csv("data/processed/y_val.csv", index=False)
y_test.to_csv("data/processed/y_test.csv", index=False)

print("Datasets saved.")

# -----------------------------
# Save Feature Names
# -----------------------------

feature_names = list(X.columns)

with open("data/processed/feature_names.json", "w") as f:
    json.dump(feature_names, f, indent=4)

print("Feature names saved.")

# -----------------------------
# Save Scaler
# -----------------------------

with open("data/processed/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Scaler saved.")

print("Model preparation completed successfully.")