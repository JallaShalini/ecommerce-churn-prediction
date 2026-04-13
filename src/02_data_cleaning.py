import json
from datetime import datetime

import pandas as pd


class DataCleaner:
    """Comprehensive data cleaning pipeline for the Online Retail dataset."""

    def __init__(self, input_path: str = "data/raw/online_retail.csv") -> None:
        self.input_path = input_path
        self.df: pd.DataFrame | None = None
        self.cleaning_stats: dict[str, object] = {
            "original_rows": 0,
            "rows_after_cleaning": 0,
            "rows_removed": 0,
            "missing_values_before": {},
            "missing_values_after": {},
            "steps_applied": [],
        }

    def load_data(self) -> "DataCleaner":
        """Load raw dataset with proper encoding and date parsing."""
        self.df = pd.read_csv(
            self.input_path,
            encoding="latin1",
            parse_dates=["InvoiceDate"],
        )

        # Normalize column names to the canonical schema used in this project
        # - Customer ID -> CustomerID
        # - Invoice -> InvoiceNo
        # - Price -> UnitPrice (if UnitPrice not already present)
        if "Customer ID" in self.df.columns and "CustomerID" not in self.df.columns:
            self.df.rename(columns={"Customer ID": "CustomerID"}, inplace=True)
        if "Invoice" in self.df.columns and "InvoiceNo" not in self.df.columns:
            self.df["InvoiceNo"] = self.df["Invoice"]
        if "Price" in self.df.columns and "UnitPrice" not in self.df.columns:
            self.df["UnitPrice"] = self.df["Price"]

        self.cleaning_stats["original_rows"] = len(self.df)
        self.cleaning_stats["missing_values_before"] = self.df.isnull().sum().to_dict()
        self.cleaning_stats["steps_applied"].append(
            {"step": "load_data", "rows_removed": 0}
        )
        return self

    def remove_missing_customer_ids(self) -> "DataCleaner":
        """Remove rows with missing CustomerID (required for customer-level features)."""
        initial_rows = len(self.df)
        self.df = self.df.dropna(subset=["CustomerID"])
        rows_removed = initial_rows - len(self.df)
        self.cleaning_stats["steps_applied"].append(
            {"step": "remove_missing_customer_ids", "rows_removed": rows_removed}
        )
        return self

    def handle_cancelled_invoices(self) -> "DataCleaner":
        """Remove cancelled invoices (InvoiceNo starting with 'C')."""
        initial_rows = len(self.df)
        self.df = self.df[~self.df["InvoiceNo"].astype(str).str.startswith("C")]
        rows_removed = initial_rows - len(self.df)
        self.cleaning_stats["steps_applied"].append(
            {"step": "handle_cancelled_invoices", "rows_removed": rows_removed}
        )
        return self

    def handle_negative_quantities(self) -> "DataCleaner":
        """Remove rows with negative quantities (returns)."""
        initial_rows = len(self.df)
        self.df = self.df[self.df["Quantity"] > 0]
        rows_removed = initial_rows - len(self.df)
        self.cleaning_stats["steps_applied"].append(
            {"step": "handle_negative_quantities", "rows_removed": rows_removed}
        )
        return self

    def handle_zero_prices(self) -> "DataCleaner":
        """Remove rows with zero or negative unit prices."""
        initial_rows = len(self.df)
        self.df = self.df[self.df["UnitPrice"] > 0]
        rows_removed = initial_rows - len(self.df)
        self.cleaning_stats["steps_applied"].append(
            {"step": "handle_zero_prices", "rows_removed": rows_removed}
        )
        return self

    def handle_missing_descriptions(self) -> "DataCleaner":
        """Remove rows with missing product descriptions."""
        initial_rows = len(self.df)
        self.df = self.df.dropna(subset=["Description"])
        rows_removed = initial_rows - len(self.df)
        self.cleaning_stats["steps_applied"].append(
            {"step": "handle_missing_descriptions", "rows_removed": rows_removed}
        )
        return self

    def remove_outliers(self) -> "DataCleaner":
        """Remove outliers in Quantity and UnitPrice using the IQR method."""
        initial_rows = len(self.df)

        # Quantity
        q1_qty = self.df["Quantity"].quantile(0.25)
        q3_qty = self.df["Quantity"].quantile(0.75)
        iqr_qty = q3_qty - q1_qty
        lower_qty = q1_qty - 1.5 * iqr_qty
        upper_qty = q3_qty + 1.5 * iqr_qty

        # UnitPrice
        q1_price = self.df["UnitPrice"].quantile(0.25)
        q3_price = self.df["UnitPrice"].quantile(0.75)
        iqr_price = q3_price - q1_price
        lower_price = q1_price - 1.5 * iqr_price
        upper_price = q3_price + 1.5 * iqr_price

        self.df = self.df[
            (self.df["Quantity"] >= lower_qty)
            & (self.df["Quantity"] <= upper_qty)
            & (self.df["UnitPrice"] >= lower_price)
            & (self.df["UnitPrice"] <= upper_price)
        ]

        rows_removed = initial_rows - len(self.df)
        self.cleaning_stats["steps_applied"].append(
            {"step": "remove_outliers", "rows_removed": rows_removed}
        )
        return self

    def remove_duplicates(self) -> "DataCleaner":
        """Remove duplicate rows."""
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        rows_removed = initial_rows - len(self.df)
        self.cleaning_stats["steps_applied"].append(
            {"step": "remove_duplicates", "rows_removed": rows_removed}
        )
        return self

    def add_derived_columns(self) -> "DataCleaner":
        """Add TotalPrice and datetime components."""
        self.df["TotalPrice"] = self.df["Quantity"] * self.df["UnitPrice"]
        self.df["Year"] = self.df["InvoiceDate"].dt.year
        self.df["Month"] = self.df["InvoiceDate"].dt.month
        self.df["DayOfWeek"] = self.df["InvoiceDate"].dt.dayofweek
        self.df["Hour"] = self.df["InvoiceDate"].dt.hour

        self.cleaning_stats["steps_applied"].append(
            {"step": "add_derived_columns", "rows_removed": 0}
        )
        return self

    def convert_data_types(self) -> "DataCleaner":
        """Convert selected columns to efficient data types."""
        self.df["CustomerID"] = self.df["CustomerID"].astype(int)
        self.df["StockCode"] = self.df["StockCode"].astype("category")
        self.df["Country"] = self.df["Country"].astype("category")
        self.cleaning_stats["steps_applied"].append(
            {"step": "convert_data_types", "rows_removed": 0}
        )
        return self

    def save_cleaned_data(self, output_path: str = "data/processed/cleaned_transactions.csv") -> "DataCleaner":
        """Save cleaned data and statistics, including the required JSON schema."""
        import os

        os.makedirs("data/processed", exist_ok=True)

        self.df.to_csv(output_path, index=False)

        self.cleaning_stats["rows_after_cleaning"] = len(self.df)
        self.cleaning_stats["rows_removed"] = (
            self.cleaning_stats["original_rows"] - self.cleaning_stats["rows_after_cleaning"]
        )
        self.cleaning_stats["missing_values_after"] = self.df.isnull().sum().to_dict()

        retention_rate = (
            self.cleaning_stats["rows_after_cleaning"]
            / self.cleaning_stats["original_rows"]
            * 100
        )

        stats_schema = {
            "original_rows": int(self.cleaning_stats["original_rows"]),
            "rows_after_cleaning": int(self.cleaning_stats["rows_after_cleaning"]),
            "rows_removed": int(self.cleaning_stats["rows_removed"]),
            "retention_rate": round(retention_rate, 2),
            "missing_values_before": self.cleaning_stats["missing_values_before"],
            "missing_values_after": self.cleaning_stats["missing_values_after"],
            "steps_applied": self.cleaning_stats["steps_applied"],
        }

        with open("data/processed/cleaning_statistics.json", "w") as f:
            json.dump(stats_schema, f, indent=4, default=str)

        print("\n" + "=" * 50)
        print("DATA CLEANING SUMMARY")
        print("=" * 50)
        print(f"Original rows: {self.cleaning_stats['original_rows']:,}")
        print(f"Cleaned rows: {self.cleaning_stats['rows_after_cleaning']:,}")
        print(f"Rows removed: {self.cleaning_stats['rows_removed']:,}")
        print(f"Retention rate: {retention_rate:.2f}%")
        print("=" * 50)
        return self

    def run_pipeline(self) -> pd.DataFrame:
        """Execute full cleaning pipeline."""
        print("Starting data cleaning pipeline...")
        self.load_data()
        self.remove_missing_customer_ids()
        self.handle_cancelled_invoices()
        self.handle_negative_quantities()
        self.handle_zero_prices()
        self.handle_missing_descriptions()
        self.remove_outliers()
        self.remove_duplicates()
        self.add_derived_columns()
        self.convert_data_types()
        self.save_cleaned_data()
        print("Data cleaning pipeline completed successfully!")
        return self.df


if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaned_df = cleaner.run_pipeline()
    print("\nCleaned dataset shape:", cleaned_df.shape)