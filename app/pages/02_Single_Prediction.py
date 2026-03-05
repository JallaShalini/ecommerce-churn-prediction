import streamlit as st
from predict import predict, predict_proba

st.title("🔮 Single Customer Prediction")

st.write("Enter customer details to predict churn.")

frequency = st.number_input("Frequency", min_value=1, max_value=100, value=5)
monetary = st.number_input("Monetary Value", min_value=0, value=500)
avg_order = st.number_input("Avg Order Value", min_value=0, value=100)
unique_products = st.number_input("Unique Products", min_value=1, value=3)

preferred_day = st.selectbox(
    "Preferred Day",
    ["Weekday","Weekend"]
)

customer_segment = st.selectbox(
    "Customer Segment",
    ["Bronze","Silver","Gold"]
)

if st.button("Predict Churn"):

    customer = {
        "Frequency":frequency,
        "Monetary":monetary,
        "AvgOrderValue":avg_order,
        "UniqueProducts":unique_products,
        "PreferredDay":preferred_day,
        "CustomerSegment":customer_segment
    }

    prediction = predict(customer)
    probability = predict_proba(customer)

    if prediction == 1:
        st.error("Customer is likely to CHURN")
    else:
        st.success("Customer is NOT likely to churn")

    st.write("Churn Probability:", round(probability,3))