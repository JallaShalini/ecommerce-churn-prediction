import streamlit as st
import pandas as pd

st.title("📈 Model Dashboard")

st.write("Model Performance Metrics")

data = {
"Metric":["ROC-AUC","Precision","Recall"],
"Score":[0.97,0.99,0.75]
}

df = pd.DataFrame(data)

st.table(df)

st.bar_chart(df.set_index("Metric"))