import pandas as pd
import json
import os
from datetime import datetime

# ------------------------------
# File paths
# ------------------------------

DATA_PATH = "data/raw/online_retail.csv"
PROFILE_PATH = "data/raw/data_profile.txt"
SUMMARY_PATH = "data/raw/data_quality_summary.json"

# ------------------------------
# Load dataset
# ------------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully.")

# ------------------------------
# Dataset basic info
# ------------------------------

rows, cols = df.shape
columns = list(df.columns)

missing_values = df.isnull().sum().to_dict()

duplicate_rows = int(df.duplicated().sum())

data_types = df.dtypes.astype(str).to_dict()

# ------------------------------
# Create data profile
# ------------------------------

profile_lines = []

profile_lines.append("DATASET PROFILE REPORT")
profile_lines.append("----------------------")
profile_lines.append(f"Generated: {datetime.now()}")
profile_lines.append("")
profile_lines.append(f"Rows: {rows}")
profile_lines.append(f"Columns: {cols}")
profile_lines.append("")
profile_lines.append("Columns:")
profile_lines.extend(columns)
profile_lines.append("")
profile_lines.append("Data Types:")
for col, dtype in data_types.items():
    profile_lines.append(f"{col}: {dtype}")
profile_lines.append("")
profile_lines.append("Missing Values:")
for col, miss in missing_values.items():
    profile_lines.append(f"{col}: {miss}")
profile_lines.append("")
profile_lines.append(f"Duplicate Rows: {duplicate_rows}")

# ------------------------------
# Save profile report
# ------------------------------

with open(PROFILE_PATH, "w") as f:
    for line in profile_lines:
        f.write(line + "\n")

print("Data profile report created.")

# ------------------------------
# Create JSON summary
# ------------------------------

summary = {
    "dataset_name": "online_retail",
    "rows": rows,
    "columns": cols,
    "column_names": columns,
    "missing_values": missing_values,
    "duplicate_rows": duplicate_rows,
    "generated_at": str(datetime.now())
}

with open(SUMMARY_PATH, "w") as f:
    json.dump(summary, f, indent=4)

print("JSON data quality summary created.")

print("Data acquisition completed successfully.")