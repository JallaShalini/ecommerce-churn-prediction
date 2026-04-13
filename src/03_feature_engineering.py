import pandas as pd
import numpy as np
import json
from datetime import timedelta


class FeatureEngineer:
    """Customer-level feature engineering with proper temporal churn definition.

    This class:
    - Splits cleaned transactions into training and observation periods
    - Defines churn based on future inactivity (no purchases in observation window)
    - Builds RFM, behavioral, temporal, and product features
    - Saves customer_features.csv and feature_info.json
    """

    def __init__(self, transactions_path="data/processed/cleaned_transactions.csv", training_window_days=90):
        self.transactions_path = transactions_path
        self.training_window_days = training_window_days

        self.transactions = pd.read_csv(self.transactions_path, parse_dates=["InvoiceDate"])

        # Use canonical column names from UCI dataset
        # Ensure CustomerID is present and numeric
        if "CustomerID" not in self.transactions.columns:
            raise ValueError("Expected 'CustomerID' column in cleaned transactions.")

        self.max_date = self.transactions["InvoiceDate"].max()
        self.training_cutoff = self.max_date - timedelta(days=self.training_window_days)
        self.observation_end = self.max_date

        self.training_data = None
        self.observation_data = None
        self.customer_features = None

        print(f"Loaded {len(self.transactions)} transactions")
        print(f"Data range: {self.transactions['InvoiceDate'].min()} to {self.max_date}")
        print(f"Training cutoff: {self.training_cutoff}")
        print(f"Observation end: {self.observation_end}")

    # ------------------------------------------------------------------
    # Temporal split & churn
    # ------------------------------------------------------------------
    def split_data_by_time(self):
        """Split transactions into training and observation periods."""
        self.training_data = self.transactions[self.transactions["InvoiceDate"] <= self.training_cutoff].copy()
        self.observation_data = self.transactions[
            (self.transactions["InvoiceDate"] > self.training_cutoff)
            & (self.transactions["InvoiceDate"] <= self.observation_end)
        ].copy()

        print(f"Training transactions: {len(self.training_data)}")
        print(f"Observation transactions: {len(self.observation_data)}")
        return self

    def create_target_variable(self):
        """Create churn label: 1 = churned, 0 = active.

        A customer is churned if they purchased in the training period
        but made no purchases in the observation period.
        """

        training_customers = set(self.training_data["CustomerID"].unique())
        observation_customers = set(self.observation_data["CustomerID"].unique())

        self.customer_features = pd.DataFrame({"CustomerID": list(training_customers)})

        self.customer_features["Churn"] = self.customer_features["CustomerID"].apply(
            lambda cid: 1 if cid not in observation_customers else 0
        )

        churn_rate = self.customer_features["Churn"].mean() * 100
        print(f"Churn rate: {churn_rate:.2f}%")
        if churn_rate < 20 or churn_rate > 40:
            print("WARNING: Churn rate is outside the typical 20–40% band. "
                  "Verify the temporal split and cleaning steps.")
        return self

    # ------------------------------------------------------------------
    # RFM and related features
    # ------------------------------------------------------------------
    def create_rfm_features(self):
        """Create classic RFM features using training period only."""
        df = self.training_data.copy()

        # Raw cleaned data uses 'Invoice' as invoice identifier
        rfm = df.groupby("CustomerID").agg(
            {
                "InvoiceDate": lambda x: (self.training_cutoff - x.max()).days,
                "Invoice": "nunique",
                "TotalPrice": ["sum", "mean"],
                "StockCode": "nunique",
                "Quantity": "sum",
            }
        ).reset_index()

        rfm.columns = [
            "CustomerID",
            "Recency",
            "Frequency",
            "TotalSpent",
            "AvgOrderValue",
            "UniqueProducts",
            "TotalItems",
        ]

        self.customer_features = self.customer_features.merge(rfm, on="CustomerID", how="left")

        print("RFM features created.")
        return self

    def create_behavioral_features(self):
        """Create behavioral features: intervals, basket stats, preferences."""
        df = self.training_data.copy()

        # Average days between purchases
        intervals = (
            df.sort_values(["CustomerID", "InvoiceDate"])
            .groupby("CustomerID")["InvoiceDate"]
            .apply(lambda x: x.diff().dt.days.mean())
            .reset_index(name="AvgDaysBetweenPurchases")
        )

        # Basket size stats per invoice
        basket = (
            df.groupby(["CustomerID", "Invoice"])["Quantity"]
            .sum()
            .groupby("CustomerID")
            .agg(["mean", "std", "max"])
            .reset_index()
        )
        basket.columns = ["CustomerID", "AvgBasketSize", "StdBasketSize", "MaxBasketSize"]

        # Preferred day (0-6) and hour (0-23)
        df["DayOfWeek"] = df["InvoiceDate"].dt.dayofweek
        df["Hour"] = df["InvoiceDate"].dt.hour

        prefs = (
            df.groupby("CustomerID")[["DayOfWeek", "Hour"]]
            .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0])
            .reset_index()
        )
        prefs.columns = ["CustomerID", "PreferredDay", "PreferredHour"]

        # Country diversity
        country_div = (
            df.groupby("CustomerID")["Country"].nunique().reset_index(name="CountryDiversity")
        )

        self.customer_features = (
            self.customer_features.merge(intervals, on="CustomerID", how="left")
            .merge(basket, on="CustomerID", how="left")
            .merge(prefs, on="CustomerID", how="left")
            .merge(country_div, on="CustomerID", how="left")
        )

        print("Behavioral features created.")
        return self

    def create_temporal_features(self):
        """Create temporal features: lifetime, velocity, recent activity windows."""
        df = self.training_data.copy()

        lifetime = (
            df.groupby("CustomerID")["InvoiceDate"]
            .agg(["min", "max"])
            .reset_index()
            .rename(columns={"min": "FirstPurchaseDate", "max": "LastPurchaseDate"})
        )
        lifetime["CustomerLifetimeDays"] = (
            lifetime["LastPurchaseDate"] - lifetime["FirstPurchaseDate"]
        ).dt.days

        # Purchase velocity = frequency / lifetime
        freq = self.customer_features.set_index("CustomerID")["Frequency"]
        lifetime["PurchaseVelocity"] = (
            freq.reindex(lifetime["CustomerID"]).values
            / (lifetime["CustomerLifetimeDays"] + 1)
        )

        # Recent activity windows (30/60/90 days before training cutoff)
        cutoff_30 = self.training_cutoff - timedelta(days=30)
        cutoff_60 = self.training_cutoff - timedelta(days=60)
        cutoff_90 = self.training_cutoff - timedelta(days=90)

        recent_30 = (
            df[df["InvoiceDate"] > cutoff_30]
            .groupby("CustomerID")["Invoice"]
            .nunique()
            .reset_index(name="Purchases_Last30Days")
        )
        recent_60 = (
            df[df["InvoiceDate"] > cutoff_60]
            .groupby("CustomerID")["Invoice"]
            .nunique()
            .reset_index(name="Purchases_Last60Days")
        )
        recent_90 = (
            df[df["InvoiceDate"] > cutoff_90]
            .groupby("CustomerID")["Invoice"]
            .nunique()
            .reset_index(name="Purchases_Last90Days")
        )

        self.customer_features = (
            self.customer_features.merge(
                lifetime[["CustomerID", "CustomerLifetimeDays", "PurchaseVelocity"]],
                on="CustomerID",
                how="left",
            )
            .merge(recent_30, on="CustomerID", how="left")
            .merge(recent_60, on="CustomerID", how="left")
            .merge(recent_90, on="CustomerID", how="left")
        )

        for col in ["Purchases_Last30Days", "Purchases_Last60Days", "Purchases_Last90Days"]:
            self.customer_features[col] = self.customer_features[col].fillna(0)

        print("Temporal features created.")
        return self

    def create_product_features(self):
        """Create product affinity and price preference features."""
        df = self.training_data.copy()

        # Diversity ratio: unique products / total rows
        prod_div = (
            df.groupby("CustomerID")["StockCode"]
            .agg(lambda x: len(set(x)) / len(x))
            .reset_index(name="ProductDiversityScore")
        )

        price_col = "UnitPrice" if "UnitPrice" in df.columns else "Price"
        price_pref = (
            df.groupby("CustomerID")[price_col]
            .agg(["mean", "std", "min", "max"])
            .reset_index()
        )
        price_pref.columns = [
            "CustomerID",
            "AvgPricePreference",
            "StdPricePreference",
            "MinPrice",
            "MaxPrice",
        ]

        qty_pref = (
            df.groupby(["CustomerID", "Invoice"])["Quantity"]
            .sum()
            .groupby("CustomerID")
            .mean()
            .reset_index(name="AvgQuantityPerOrder")
        )

        self.customer_features = (
            self.customer_features.merge(prod_div, on="CustomerID", how="left")
            .merge(price_pref, on="CustomerID", how="left")
            .merge(qty_pref, on="CustomerID", how="left")
        )

        print("Product features created.")
        return self

    def create_customer_value_segment(self):
        """Create RFM scores and customer segments."""
        cf = self.customer_features

        cf["RecencyScore"] = pd.qcut(
            cf["Recency"], q=4, labels=[4, 3, 2, 1], duplicates="drop"
        ).astype(int)
        # For Frequency/Monetary we may have low cardinality; use rank to avoid
        # duplicate bin edges in qcut.
        cf["FrequencyScore"] = pd.qcut(
            cf["Frequency"].rank(method="first"),
            q=4,
            labels=[1, 2, 3, 4],
            duplicates="drop",
        ).astype(int)

        cf["MonetaryScore"] = pd.qcut(
            cf["TotalSpent"].rank(method="first"),
            q=4,
            labels=[1, 2, 3, 4],
            duplicates="drop",
        ).astype(int)

        cf["RFM_Score"] = (
            cf["RecencyScore"] + cf["FrequencyScore"] + cf["MonetaryScore"]
        )

        def segment(row):
            if row["RFM_Score"] >= 10:
                return "Champions"
            if row["RFM_Score"] >= 8:
                return "Loyal"
            if row["RFM_Score"] >= 6:
                return "Potential"
            if row["RFM_Score"] >= 4:
                return "At Risk"
            return "Lost"

        cf["CustomerSegment"] = cf.apply(segment, axis=1)

        self.customer_features = cf
        print("Customer segments created.")
        return self

    def handle_missing_values(self):
        """Fill remaining missing values: numeric → median, categorical → mode."""
        cf = self.customer_features
        numeric_cols = [
            c for c in cf.select_dtypes(include=[np.number]).columns
            if c not in ["CustomerID", "Churn"]
        ]
        for col in numeric_cols:
            cf[col] = cf[col].fillna(cf[col].median())

        cat_cols = [
            c for c in cf.select_dtypes(exclude=[np.number]).columns
            if c not in ["CustomerID", "Churn"]
        ]
        for col in cat_cols:
            if not cf[col].mode().empty:
                cf[col] = cf[col].fillna(cf[col].mode().iloc[0])

        self.customer_features = cf
        print("Missing values handled.")
        return self

    def save_features(self, output_path="data/processed/customer_features.csv"):
        """Save customer_features.csv and feature_info.json with required schema."""
        self.customer_features.to_csv(output_path, index=False)
        print(f"Customer features saved to {output_path}.")

        churn_rate = float(self.customer_features["Churn"].mean())
        churned = int(self.customer_features["Churn"].sum())
        total_customers = int(len(self.customer_features))

        feature_categories = {
            "rfm": [
                "Recency",
                "Frequency",
                "TotalSpent",
                "AvgOrderValue",
                "UniqueProducts",
                "TotalItems",
            ],
            "behavioral": [
                "AvgDaysBetweenPurchases",
                "AvgBasketSize",
                "StdBasketSize",
                "MaxBasketSize",
                "PreferredDay",
                "PreferredHour",
                "CountryDiversity",
            ],
            "temporal": [
                "CustomerLifetimeDays",
                "PurchaseVelocity",
                "Purchases_Last30Days",
                "Purchases_Last60Days",
                "Purchases_Last90Days",
            ],
            "product": [
                "ProductDiversityScore",
                "AvgPricePreference",
                "StdPricePreference",
                "MinPrice",
                "MaxPrice",
                "AvgQuantityPerOrder",
            ],
            "derived": [
                "RecencyScore",
                "FrequencyScore",
                "MonetaryScore",
                "RFM_Score",
                "CustomerSegment",
            ],
        }

        feature_list = list(self.customer_features.columns)
        total_feature_count = len(feature_list) - 2  # exclude CustomerID & Churn

        feature_info = {
            "total_features": total_feature_count,
            "feature_categories": {k: len(v) for k, v in feature_categories.items()},
            "churn_rate": churn_rate,
            "training_cutoff": str(self.training_cutoff.date()),
            "observation_end": str(self.observation_end.date()),
            "training_customers": total_customers,
            "churned_customers": churned,
            "active_customers": total_customers - churned,
            "features": [
                {
                    "name": "Recency",
                    "type": "numeric",
                    "description": "Days since last purchase in training period",
                    "min": float(self.customer_features["Recency"].min()),
                    "max": float(self.customer_features["Recency"].max()),
                    "mean": float(self.customer_features["Recency"].mean()),
                }
            ],
        }

        with open("data/processed/feature_info.json", "w") as f:
            json.dump(feature_info, f, indent=4)

        print("feature_info.json saved.")
        print("Feature engineering summary:")
        print(f"  Customers: {total_customers}")
        print(f"  Features (excluding IDs/target): {total_feature_count}")
        print(f"  Churn rate: {churn_rate * 100:.2f}%")
        return self

    def run_pipeline(self):
        print("=" * 60)
        print("STARTING FEATURE ENGINEERING PIPELINE")
        print("=" * 60)

        self.split_data_by_time()
        self.create_target_variable()
        self.create_rfm_features()
        self.create_behavioral_features()
        self.create_temporal_features()
        self.create_product_features()
        self.create_customer_value_segment()
        self.handle_missing_values()
        self.save_features()

        print("Feature engineering completed successfully.")
        return self.customer_features


if __name__ == "__main__":
    engineer = FeatureEngineer()
    customer_features = engineer.run_pipeline()