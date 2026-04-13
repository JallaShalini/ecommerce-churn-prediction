import streamlit as st
import pandas as pd

from predict import predict, predict_proba, load_feature_names

st.title("📂 Batch Prediction")

st.write(
    "Upload a CSV with aggregated customer features. At minimum, the file must include "
    "the following columns: Recency, Frequency, TotalSpent, AvgOrderValue, UniqueProducts, "
    "CustomerLifetimeDays, PurchaseVelocity, Purchases_Last90Days, PreferredDay, PreferredHour, CustomerSegment."
)

REQUIRED_COLUMNS = [
    "Recency",
    "Frequency",
    "TotalSpent",
    "AvgOrderValue",
    "UniqueProducts",
    "CustomerLifetimeDays",
    "PurchaseVelocity",
    "Purchases_Last90Days",
    "PreferredDay",
    "PreferredHour",
    "CustomerSegment",
]

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        st.error(f"The uploaded file is missing required columns: {', '.join(missing_cols)}")
    else:
        st.success("File loaded successfully. Columns look valid.")

        predictions = []
        probabilities = []

        for _, row in df.iterrows():
            customer = row.to_dict()
            pred = predict(customer)
            proba = predict_proba(customer)
            predictions.append(pred)
            probabilities.append(proba)

        df["Prediction"] = predictions
        df["Churn_Probability"] = probabilities

        st.write(df)

        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Results as CSV",
            data=csv_bytes,
            file_name="batch_predictions.csv",
            mime="text/csv",
        )