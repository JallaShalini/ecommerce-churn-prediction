import streamlit as st
from predict import predict, predict_proba

st.title("🔮 Single Customer Prediction")

st.write("Enter aggregated customer features to predict churn.")

recency = st.number_input(
    "Recency (days since last purchase)", min_value=0, max_value=365, value=90
)
frequency = st.number_input(
    "Frequency (total number of orders)", min_value=1, max_value=100, value=5
)
total_spent = st.number_input(
    "Total Spent", min_value=0.0, value=500.0
)
avg_order_value = st.number_input(
    "Average Order Value", min_value=0.0, value=100.0
)
unique_products = st.number_input(
    "Unique Products Purchased", min_value=1, value=10
)
customer_lifetime_days = st.number_input(
    "Customer Lifetime (days)", min_value=0, value=180
)
purchase_velocity = st.number_input(
    "Purchase Velocity (orders per day)", min_value=0.0, value=0.02
)
purchases_last_90 = st.number_input(
    "Purchases in Last 90 Days", min_value=0, value=1
)
preferred_day = st.number_input(
    "Preferred Day of Week (0 = Mon, 6 = Sun)", min_value=0, max_value=6, value=2
)
preferred_hour = st.number_input(
    "Preferred Hour of Day (0-23)", min_value=0, max_value=23, value=12
)

customer_segment = st.selectbox(
    "Customer Segment",
    ["At Risk", "Champions", "Lost", "Loyal", "Potential"],
)

if st.button("Predict Churn"):

    customer = {
        "Recency": recency,
        "Frequency": frequency,
        "TotalSpent": total_spent,
        "AvgOrderValue": avg_order_value,
        "UniqueProducts": unique_products,
        "CustomerLifetimeDays": customer_lifetime_days,
        "PurchaseVelocity": purchase_velocity,
        "Purchases_Last90Days": purchases_last_90,
        "PreferredDay": preferred_day,
        "PreferredHour": preferred_hour,
        "CustomerSegment": customer_segment,
    }

    prediction = predict(customer)
    probability = predict_proba(customer)

    if prediction == 1:
        st.error("Customer is likely to CHURN")
        st.write("Recommendation: Prioritize this customer for a retention offer.")
    else:
        st.success("Customer is NOT likely to churn")
        st.write("Recommendation: Maintain current engagement level.")

    st.write("Churn Probability:", round(probability, 3))