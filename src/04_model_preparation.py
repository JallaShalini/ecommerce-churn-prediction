import json
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


INPUT_FILE = "data/processed/customer_features.csv"


def main() -> None:
    """Prepare data for modeling.

    - Load customer_features.csv (with CustomerID and Churn already defined)
    - One-hot encode CustomerSegment
    - Keep PreferredDay/PreferredHour as numeric
    - Stratified train/val/test split (70/15/15)
    - Scale numeric features only
    - Save X/y splits, feature_names.json, and scaler.pkl
    """

    print("Loading customer features...")
    df = pd.read_csv(INPUT_FILE)
    print("Dataset shape:", df.shape)

    if "Churn" not in df.columns:
        raise ValueError("Expected 'Churn' column in customer_features.csv. Run feature engineering first.")

    # Keep CustomerID only for reference; drop from feature matrix
    if "CustomerID" in df.columns:
        df_features = df.drop(columns=["CustomerID"])
    else:
        df_features = df.copy()

    # Separate target
    y = df_features["Churn"].astype(int)
    X = df_features.drop(columns=["Churn"])

    # One-hot encode CustomerSegment; keep other numerical as-is
    if "CustomerSegment" in X.columns:
        segment_dummies = pd.get_dummies(X["CustomerSegment"], prefix="Segment")
        X = pd.concat([X.drop(columns=["CustomerSegment"]), segment_dummies], axis=1)

    print("Features after encoding:", X.shape[1])

    # Stratified split: 70% train, 15% val, 15% test
    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        stratify=y,
        random_state=42,
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        stratify=y_temp,
        random_state=42,
    )

    print("Train size:", X_train.shape)
    print("Validation size:", X_val.shape)
    print("Test size:", X_test.shape)

    # Scale numeric features only (leave one-hot dummies like Segment_* as they are)
    numeric_cols = [
        c
        for c in X.select_dtypes(include=["int64", "float64"]).columns
        if not c.startswith("Segment_")
    ]
    scaler = StandardScaler()

    X_train_scaled = X_train.copy()
    X_val_scaled = X_val.copy()
    X_test_scaled = X_test.copy()

    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_val_scaled[numeric_cols] = scaler.transform(X_val[numeric_cols])
    X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])

    # Save datasets
    X_train_scaled.to_csv("data/processed/X_train.csv", index=False)
    X_val_scaled.to_csv("data/processed/X_val.csv", index=False)
    X_test_scaled.to_csv("data/processed/X_test.csv", index=False)

    y_train.to_csv("data/processed/y_train.csv", index=False)
    y_val.to_csv("data/processed/y_val.csv", index=False)
    y_test.to_csv("data/processed/y_test.csv", index=False)

    print("Datasets saved.")

    # Save feature names
    feature_names = list(X.columns)
    with open("data/processed/feature_names.json", "w") as f:
        json.dump(feature_names, f, indent=4)
    print("Feature names saved.")

    # Save scaler in models directory for deployment
    with open("models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    print("Scaler saved to models/scaler.pkl.")

    # Summary
    def churn_rate(series):
        return float(series.mean() * 100)

    print("\nData Preparation Summary:")
    print(f"- Original features: {df_features.shape[1] - 1}")  # minus Churn
    print(f"- Features after encoding: {len(feature_names)}")
    print(f"- Training samples: {len(X_train)}")
    print(f"- Validation samples: {len(X_val)}")
    print(f"- Test samples: {len(X_test)}")
    print(f"- Churn rate in train: {churn_rate(y_train):.2f}%")
    print(f"- Churn rate in validation: {churn_rate(y_val):.2f}%")
    print(f"- Churn rate in test: {churn_rate(y_test):.2f}%")


if __name__ == "__main__":
    main()