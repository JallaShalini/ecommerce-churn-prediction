📊 E-commerce Customer Churn Prediction System
============================================

## 1. Business Overview

E-commerce businesses depend heavily on repeat purchases. Acquiring a new
customer is much more expensive than retaining an existing one, so being able
to **predict which customers are likely to churn in the next 90 days** is
critical.

This project builds an **end-to-end machine learning system** that:

- Defines churn as **no purchases in the 90 days following an observation
	window**.
- Engineers rich behavioral features from transaction data
	(Recency/Frequency/Monetary and beyond).
- Trains and evaluates several models and selects a final deployed model.
- Exposes predictions via a **Streamlit web application** and a Python
	prediction API.

The primary business goal is to help the marketing team prioritize **at‑risk
customers for retention campaigns**, improving customer lifetime value while
controlling campaign costs.

---

## 2. Dataset Information

- **Source:** Online retail transaction dataset (e-commerce orders)
- **Raw file:** `data/raw/online_retail.csv`
- **Shape:** 541,910 rows × 8 columns

Key raw columns:

| Column      | Description                                   |
|-------------|-----------------------------------------------|
| Invoice     | Unique transaction ID                         |
| StockCode   | Product identifier                            |
| Description | Product name                                  |
| Quantity    | Number of items purchased (positive integer)  |
| InvoiceDate | Date and time of purchase                     |
| Price       | Price per item                                |
| Customer ID | Unique customer identifier                    |
| Country     | Customer location                             |

From this transactional data, we aggregate at the **customer level** to
create features such as Recency, Frequency, TotalSpent, temporal activity,
purchase velocity, and RFM-based segments.

---

## 3. Methodology (Pipeline Summary)

The project follows a reproducible, script-driven pipeline:

1. **Data Acquisition** – [src/01_data_acquisition.py](src/01_data_acquisition.py)
	 - Loads raw CSV from `data/raw/online_retail.csv`.
	 - Generates an initial data profile and data quality summary JSON.

2. **Data Cleaning** – [src/02_data_cleaning.py](src/02_data_cleaning.py)
	 - Implements a `DataCleaner` class.
	 - Removes invalid rows (missing customer IDs, negative quantities/prices,
		 cancelled invoices, duplicates).
	 - Standardizes data types and adds derived transaction-level fields.
	 - Outputs `data/processed/cleaned_transactions.csv` and
		 `data/processed/cleaning_statistics.json`.

3. **Feature Engineering & Churn Definition** – [src/03_feature_engineering.py](src/03_feature_engineering.py)
	 - Implements a `FeatureEngineer` class.
	 - Uses a **temporal split**: defines a training window and a 90‑day
		 observation window to avoid data leakage.
	 - Creates RFM, behavioral, temporal, and product diversity features per
		 customer.
	 - Defines the binary `Churn` label based on inactivity in the observation
		 window.
	 - Outputs `data/processed/customer_features.csv` and
		 `data/processed/feature_info.json`.

4. **Model Preparation** – [src/04_model_preparation.py](src/04_model_preparation.py)
	 - Loads `customer_features.csv`.
	 - Drops `CustomerID` from the feature matrix but keeps it in the file.
	 - One‑hot encodes `CustomerSegment` into `Segment_*` columns.
	 - Performs a **stratified train/validation/test split** (70/15/15).
	 - Scales only numeric features (excluding `Segment_*` dummies) using
		 `StandardScaler`.
	 - Saves `X_train.csv`, `X_val.csv`, `X_test.csv`, `y_train.csv`,
		 `y_val.csv`, `y_test.csv`, and `feature_names.json` under
		 `data/processed/`, and `models/scaler.pkl`.

5. **Model Development & Evaluation** – notebooks
	 - [notebooks/04_baseline_model.ipynb](notebooks/04_baseline_model.ipynb):
		 Logistic Regression baseline.
	 - [notebooks/05_advanced_models.ipynb](notebooks/05_advanced_models.ipynb):
		 Decision Tree, Random Forest, XGBoost, Neural Network.
	 - [notebooks/06_model_evaluation.ipynb](notebooks/06_model_evaluation.ipynb):
		 evaluation of the selected model on the **test set** with confusion
		 matrix, ROC curve, precision–recall curve, calibration plots, and
		 misclassification analysis.
	 - [notebooks/07_cross_validation.ipynb](notebooks/07_cross_validation.ipynb):
		 5‑fold stratified cross‑validation using the final model.

6. **Deployment (API + Streamlit)** – [app](app)
	 - `app/predict.py` exposes a Python API that mirrors the training
		 preprocessing (segment encoding, scaling, feature ordering).
	 - `app/streamlit_app.py` and `app/pages/` provide:
		 - Home and documentation pages.
		 - Single-customer prediction form.
		 - Batch prediction via CSV upload.
		 - Model dashboard with metrics and plots.

---

## 4. Final Model and Performance

- **Final model:** Logistic Regression (selected based on validation
	performance and stability).
- **Input features:** 33 engineered features including Recency, Frequency,
	TotalSpent, temporal and behavioral metrics, and segment dummies.

On the held‑out test set, the model achieves approximately:

- ROC-AUC: ~0.77
- Accuracy: ~0.69
- Precision: ~0.64
- Recall: ~0.66
- F1-score: ~0.65

These values are consistent with the evaluation notebook and used in the
business impact analysis.

Deployment details (platform and URL) are recorded in
[`submission.json`](submission.json).

---

## 5. Installation and Usage

### 5.1 Local Setup

```bash
git clone https://github.com/JallaShalini/ecommerce-churn-prediction.git
cd ecommerce-churn-prediction

python -m venv venv
venv/Scripts/activate  # On Windows
pip install -r requirements.txt
```

Then run the core pipeline (optional, if you want to regenerate artifacts):

```bash
venv/Scripts/python.exe src/01_data_acquisition.py
venv/Scripts/python.exe src/02_data_cleaning.py
venv/Scripts/python.exe src/03_feature_engineering.py
venv/Scripts/python.exe src/04_model_preparation.py
```

### 5.2 Running the Streamlit App Locally

From the project root:

```bash
venv/Scripts/python.exe -m streamlit run app/streamlit_app.py
```

Then open the URL printed in the terminal, typically
http://localhost:8501.

### 5.3 Docker Usage

This repository includes a `Dockerfile` and `docker-compose.yml`.

Build and run with Docker:

```bash
docker build -t ecommerce-churn-app .
docker run -p 8501:8501 ecommerce-churn-app
```

Or using docker-compose:

```bash
docker-compose up --build
```

Then access the app at http://localhost:8501.

---

## 6. Live Application

The project is configured for deployment to **Streamlit Cloud**.

- Live app URL (from `submission.json`):
	https://ecommerce-churn-prediction-htezfjcg74hsh5qdw64s9n.streamlit.app

Use this link to interact with the deployed churn prediction application
directly in your browser.
