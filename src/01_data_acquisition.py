import json
import os
from datetime import datetime

import pandas as pd


RAW_DATA_PATH = "data/raw/online_retail.csv"
PROFILE_PATH = "data/raw/data_profile.txt"
SUMMARY_PATH = "data/raw/data_quality_summary.json"


def download_dataset() -> str:
    """Download or locate the raw dataset and save it as online_retail.csv.

    In this project we assume the UCI/Kaggle file has been downloaded
    manually into the repository. This function simply ensures the
    expected CSV exists and returns its path.

    If the file is missing, it raises a clear error telling the user
    where to place the dataset.
    """

    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)

    if os.path.exists(RAW_DATA_PATH):
        print(f"Raw dataset already present at {RAW_DATA_PATH}.")
        return RAW_DATA_PATH

    raise FileNotFoundError(
        "Raw dataset not found. Please place the Online Retail CSV from "
        "UCI/Kaggle at 'data/raw/online_retail.csv' and rerun this script."
    )


def load_raw_data() -> pd.DataFrame:
    """Load the raw dataset from CSV.

    Assumes the file has already been downloaded to data/raw/online_retail.csv
    from UCI or Kaggle.
    """

    return pd.read_csv(RAW_DATA_PATH, encoding="latin1")


def generate_data_profile(df: pd.DataFrame) -> None:
    """Generate a human-readable profile in data/raw/data_profile.txt."""

    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)

    rows, cols = df.shape
    missing_values = df.isnull().sum().to_dict()
    data_types = df.dtypes.astype(str).to_dict()
    duplicate_rows = int(df.duplicated().sum())

    lines: list[str] = []
    lines.append("DATASET PROFILE REPORT")
    lines.append("----------------------")
    lines.append(f"Generated: {datetime.now()}")
    lines.append("")
    lines.append(f"Rows: {rows}")
    lines.append(f"Columns: {cols}")
    lines.append("")
    lines.append("Columns:")
    lines.extend(list(df.columns))
    lines.append("")
    lines.append("Data Types:")
    for col, dtype in data_types.items():
        lines.append(f"{col}: {dtype}")
    lines.append("")
    lines.append("Missing Values:")
    for col, miss in missing_values.items():
        lines.append(f"{col}: {miss}")
    lines.append("")
    lines.append(f"Duplicate Rows: {duplicate_rows}")

    with open(PROFILE_PATH, "w") as f:
        for line in lines:
            f.write(line + "\n")


def generate_data_quality_summary(df: pd.DataFrame) -> None:
    """Create data_quality_summary.json with the required schema."""

    os.makedirs(os.path.dirname(SUMMARY_PATH), exist_ok=True)

    total_rows = int(len(df))
    total_columns = int(len(df.columns))

    missing_values = df.isnull().sum().to_dict()
    duplicate_rows = int(df.duplicated().sum())

    # Map to canonical names used in the project spec
    # Raw file columns: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country
    date_min = df["InvoiceDate"].min()
    date_max = df["InvoiceDate"].max()

    negative_quantities = int((df["Quantity"] < 0).sum())
    cancelled_invoices = int(df["Invoice"].astype(str).str.startswith("C").sum())
    missing_customer_ids = int(df["Customer ID"].isnull().sum())
    missing_customer_ids_pct = round(missing_customer_ids / total_rows * 100, 1)

    summary = {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "date_range": {
            "start": str(date_min.date()) if hasattr(date_min, "date") else str(date_min),
            "end": str(date_max.date()) if hasattr(date_max, "date") else str(date_max),
        },
        "negative_quantities": negative_quantities,
        "cancelled_invoices": cancelled_invoices,
        "missing_customer_ids": missing_customer_ids,
        "missing_customer_ids_percentage": missing_customer_ids_pct,
    }

    with open(SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=4, default=str)


if __name__ == "__main__":
    print("Ensuring raw dataset is available...")
    download_dataset()

    print("Loading raw dataset...")
    df_raw = load_raw_data()
    print("Dataset loaded.")

    # Ensure InvoiceDate is parsed for date_range and profile
    df_raw["InvoiceDate"] = pd.to_datetime(df_raw["InvoiceDate"], errors="coerce")

    generate_data_profile(df_raw)
    print("Data profile written to", PROFILE_PATH)

    generate_data_quality_summary(df_raw)
    print("Data quality summary written to", SUMMARY_PATH)

    print("Data acquisition step completed successfully.")