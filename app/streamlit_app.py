import streamlit as st

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Churn Prediction System")

st.write("""
Welcome to the **E-commerce Customer Churn Prediction App**.

Use the sidebar to navigate through the application.

Available Pages:
- Home
- Single Prediction
- Batch Prediction
- Model Dashboard
- Documentation
""")