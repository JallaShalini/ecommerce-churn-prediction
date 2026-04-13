import streamlit as st

st.title("📚 Project Documentation")

st.write(
		"""
### Project Overview

This project predicts **customer churn for an e-commerce platform** using
transactional data. Customers are labeled as churned when they have **no
purchases in the 90 days following the observation window**.

### Machine Learning Pipeline

1. Data Acquisition (raw online retail transactions)
2. Data Cleaning (filtering invalid rows and fixing types)
3. Feature Engineering (RFM, behavioral, temporal, and segment features)
4. Model Preparation (train/validation/test split and scaling)
5. Model Training & Cross-Validation (Logistic Regression and baselines)
6. Evaluation on a held-out test set
7. Deployment via a prediction API and this Streamlit app

### Deployed Model

- Algorithm: **Logistic Regression** (selected based on validation ROC-AUC and
	balanced precision/recall)
- Input: aggregated customer-level features such as Recency, Frequency,
	TotalSpent, AvgOrderValue, PurchaseVelocity, Purchases_Last90Days,
	customer lifetime, and RFM-based segment.

### Current Test Performance (Approximate)

- ROC-AUC: ~0.77  
- Accuracy: ~0.69  
- Precision: ~0.64  
- Recall: ~0.66  
- F1-score: ~0.65

See the **Model Dashboard** page for metrics computed directly from the
latest model and test split, and the **Business Impact Analysis** document in
the `docs` folder for a detailed ROI discussion.
"""
)