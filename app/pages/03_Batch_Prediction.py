import streamlit as st
import pandas as pd
from predict import predict

st.title("📂 Batch Prediction")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    predictions = []

    for _,row in df.iterrows():

        customer = row.to_dict()

        pred = predict(customer)

        predictions.append(pred)

    df["Prediction"] = predictions

    st.write(df)

    st.download_button(
        "Download Results",
        df.to_csv(index=False),
        "predictions.csv"
    )