# Slide 1 – Title & Overview

- Project: E-commerce Customer Churn Prediction
- Goal: Predict which customers are likely to churn in the next 90 days
- Stack: Python, pandas, scikit-learn, XGBoost, Streamlit
- Deployed as a Streamlit web app

---

# Slide 2 – Business Problem

- Retaining customers is cheaper than acquiring new ones
- Marketing team needs to know **which customers are at risk**
- Objective: Enable targeted retention campaigns to reduce churn
- Success: Achieve ROC-AUC > 0.75 with balanced precision/recall

---

# Slide 3 – Dataset & Churn Definition

- Source: Online retail transaction dataset
- Size: 541,910 rows × 8 columns (transactions)
- Customer-level aggregation used for modeling
- Churn definition:
  - A customer is **churned** if they have **no purchases in the 90 days**
    after the observation window

---

# Slide 4 – Data Pipeline

- 01_data_acquisition.py: load raw data and profile it
- 02_data_cleaning.py: DataCleaner to remove invalid rows & fix types
- 03_feature_engineering.py: FeatureEngineer to build RFM & behavioral features
- 04_model_preparation.py: stratified splitting + scaling + feature_names
- Notebooks: modeling, evaluation, cross-validation

(Visual: pipeline diagram from raw CSV → cleaned → features → splits → model)

---

# Slide 5 – Feature Engineering Highlights

- RFM: Recency, Frequency, TotalSpent, RFM_Score
- Behavioral: TotalItems, AvgBasketSize, CountryDiversity, ProductDiversity
- Temporal: Purchases_Last30/60/90Days, PreferredDay, PreferredHour
- Segmentation: RecencyScore, FrequencyScore, MonetaryScore, CustomerSegment

(Visuals from notebooks/03_feature_eda.ipynb: churn vs RFM plots)

---

# Slide 6 – Modeling Approach

- Train/validation/test split (70/15/15) with stratification on Churn
- Models tested:
  - Logistic Regression (baseline)
  - Decision Tree, Random Forest
  - XGBoost
  - Simple Neural Network (MLP)
- Metrics: ROC-AUC, Precision, Recall, F1-score

(Visual: comparison table/bar chart from model selection notebook)

---

# Slide 7 – Final Model & Test Performance

- Final model: **Logistic Regression**
- Input: 33 engineered features (numeric + Segment_* dummies)
- Test set performance (approx.):
  - ROC-AUC: ~0.77
  - Accuracy: ~0.69
  - Precision: ~0.64
  - Recall: ~0.66
  - F1-score: ~0.65

(Visuals from notebooks/06_model_evaluation.ipynb: ROC curve, confusion matrix)

---

# Slide 8 – Cross-Validation & Stability

- 5-fold StratifiedKFold on training data
- Model: Logistic Regression
- Per-fold ROC-AUC values clustered ~0.97 (on scaled training splits)
- Conclusion: Stable performance and low variance across folds

(Visual: ROC-AUC per fold plot from notebooks/07_cross_validation.ipynb)

---

# Slide 9 – Business Impact

- Confusion matrix on test set used to estimate impact
- Example assumptions:
  - Avg customer margin: $120/year
  - Retention campaign cost: $10 per contacted customer
  - Save probability for correctly targeted churners: 25%
- Result: Positive net gain when using the model to target at-risk customers

(Visuals/figures based on docs/12_business_impact_analysis.md)

---

# Slide 10 – Deployment & Demo

- Deployed as a Streamlit app
- Features:
  - Single-customer prediction form
  - Batch CSV upload and scoring
  - Model dashboard with metrics and plots
- Live URL:
  - https://ecommerce-churn-prediction-htezfjcg74hsh5qdw64s9n.streamlit.app

(Screenshot of the Streamlit app home/dashboard)

---

# Slide 11 – Technical Architecture

- Python scripts for data pipeline (src/)
- Processed data and artifacts in data/processed/ and models/
- Prediction logic in app/predict.py
- UI in app/streamlit_app.py and app/pages
- Optional Docker deployment with Dockerfile + docker-compose.yml

(Visual: simple architecture diagram)

---

# Slide 12 – Learnings & Next Steps

- Key learnings:
  - Importance of leakage-free churn definition
  - Value of rich behavioral features for prediction
  - Trade-offs between model complexity and interpretability
  - Practical challenges in deployment (paths, dependencies, environment)
- Future work:
  - Calibrated probability thresholds by segment
  - A/B testing of retention strategies informed by the model
  - Additional features (text, marketing interactions)
