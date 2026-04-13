# Technical Documentation

This document provides a deeper technical view of the end-to-end churn
prediction system: data pipeline, model architecture, deployment, and
troubleshooting tips.

---

## 1. Data Pipeline Overview

The data pipeline is implemented as a series of Python scripts and notebooks
that operate on the project’s `data/` directory.

### 1.1 High-Level Flow

`data/raw/online_retail.csv` → 01_data_acquisition → 02_data_cleaning →
03_feature_engineering → 04_model_preparation → modeling notebooks → Streamlit
app.

In more detail:

1. **Data Acquisition** – `src/01_data_acquisition.py`
	 - Loads `data/raw/online_retail.csv` with encoding handling.
	 - Performs initial profiling and generates:
		 - `data/raw/data_profile.txt`
		 - `data/raw/data_quality_summary.json`

2. **Data Cleaning** – `src/02_data_cleaning.py`
	 - `DataCleaner` class encapsulates all cleaning steps:
		 - Drop rows with missing `Customer ID`.
		 - Remove cancelled invoices and negative quantities/prices.
		 - Standardize column names and data types.
		 - Remove duplicates and obvious outliers.
	 - Outputs:
		 - `data/processed/cleaned_transactions.csv`
		 - `data/processed/cleaning_statistics.json` (step-by-step row counts and
			 retention rate).

3. **Feature Engineering & Churn Definition** – `src/03_feature_engineering.py`
	 - `FeatureEngineer` class:
		 - Computes `max_date` and defines a training cutoff and a 90‑day
			 observation window.
		 - Aggregates transaction-level data into customer-level features
			 including:
			 - **RFM**: `Recency`, `Frequency`, `TotalSpent`, `RFM_Score`.
			 - **Behavioral**: `TotalItems`, `AvgBasketSize`, `CountryDiversity`,
				 `ProductDiversityScore`, `PurchaseVelocity`.
			 - **Temporal**: `Purchases_Last30Days`, `Purchases_Last60Days`,
				 `Purchases_Last90Days`, `PreferredDay`, `PreferredHour`.
			 - **Segmentation**: `RecencyScore`, `FrequencyScore`, `MonetaryScore`,
				 `CustomerSegment`.
		 - Creates the binary `Churn` target based on no purchases in the
			 observation window.
	 - Outputs:
		 - `data/processed/customer_features.csv`
		 - `data/processed/feature_info.json` (per-feature metadata).

4. **Model Preparation** – `src/04_model_preparation.py`
	 - Loads `customer_features.csv` and uses `Churn` as the target.
	 - Drops `CustomerID` from the feature matrix.
	 - One-hot encodes `CustomerSegment` into `Segment_*` columns.
	 - Performs stratified splitting into train/validation/test (70/15/15).
	 - Fits a `StandardScaler` on numeric features (excluding `Segment_*`).
	 - Saves processed splits and artifacts:
		 - `data/processed/X_train.csv`, `X_val.csv`, `X_test.csv`
		 - `data/processed/y_train.csv`, `y_val.csv`, `y_test.csv`
		 - `data/processed/feature_names.json`
		 - `models/scaler.pkl`

5. **Modeling & Evaluation** – Jupyter notebooks
	 - `notebooks/04_baseline_model.ipynb`: trains a Logistic Regression model
		 and establishes baseline metrics.
	 - `notebooks/05_advanced_models.ipynb`: evaluates Decision Tree, Random
		 Forest, XGBoost, and a simple neural network; compares to baseline.
	 - `notebooks/06_model_evaluation.ipynb`: evaluates the selected model on
		 `X_test` and `y_test`, generating metrics and plots.
	 - `notebooks/07_cross_validation.ipynb`: runs 5‑fold `StratifiedKFold`
		 cross-validation using Logistic Regression and reports per-fold ROC-AUC
		 and mean/std.

6. **Deployment & Serving** – Streamlit app and prediction module
	 - `app/predict.py`: reusable prediction API.
	 - `app/streamlit_app.py` and `app/pages/`: user interface.

---

## 2. Model Architecture

### 2.1 Candidate Models

The following models were implemented and compared using the prepared
training/validation splits:

- Logistic Regression (baseline and final model)
- Decision Tree Classifier
- Random Forest Classifier
- XGBoost Classifier
- Multi-layer Perceptron (simple neural network)

Each model was evaluated using ROC-AUC, Precision, Recall, and F1-score on the
validation set.

### 2.2 Final Model Choice

The final deployed model is **Logistic Regression**, chosen because:

- It achieved competitive ROC-AUC on validation (~0.76–0.78) with balanced
	precision and recall.
- It generalized well to the test set (ROC-AUC ~0.77, F1 ~0.65) without
	overfitting.
- It is simple, interpretable, and efficient to run in a real-time setting.

### 2.3 Key Hyperparameters

For Logistic Regression (scikit-learn):

- `penalty="l2"`
- `solver="lbfgs"`
- `max_iter=1000`
- `class_weight=None` (class imbalance handled via threshold and evaluation)

For tree-based and other models, default or modestly tuned hyperparameters
were used, but they did not outperform Logistic Regression on validation and
test ROC-AUC.

### 2.4 Input and Output Schema

The model expects a feature vector with the same column order as
`data/processed/feature_names.json`. This includes:

- Numeric features (Recency, Frequency, TotalSpent, temporal and behavioral
	metrics).
- One-hot encoded segment features (`Segment_At Risk`, `Segment_Champions`,
	`Segment_Lost`, `Segment_Loyal`, `Segment_Potential`).

Outputs:

- `predict`: binary churn label (0 = non-churner, 1 = churner).
- `predict_proba`: probability of churn in the positive class.

---

## 3. Deployment Architecture

The deployment is intentionally lightweight and reproducible.

### 3.1 Components

- **Model artifacts** (under `models/` and `data/processed/`):
	- `models/best_model.pkl` – serialized Logistic Regression model.
	- `models/scaler.pkl` – `StandardScaler` fitted on training numeric
		features.
	- `data/processed/feature_names.json` – expected feature order.
- **Prediction API** – `app/predict.py`:
	- Loads model, scaler, and feature names.
	- Implements `preprocess_input` to:
		- Build a one-row DataFrame from input.
		- One-hot encode `CustomerSegment` with the same prefix and categories.
		- Add any missing columns with 0.
		- Apply the scaler to numeric features only (excluding `Segment_*`).
		- Reorder columns to match `feature_names`.
- **Streamlit app** – `app/streamlit_app.py` and `app/pages/`:
	- Single prediction page – manual entry of engineered features.
	- Batch prediction page – CSV upload, validation, and batch scoring.
	- Model dashboard – loads `X_test`, `y_test`, and `best_model.pkl` to
		recompute and display metrics and plots.
	- Documentation page – project overview, pipeline description, and links.

### 3.2 Execution Paths

1. Local execution:
	 - `streamlit run app/streamlit_app.py`
2. Containerized execution (optional):
	 - `docker build -t ecommerce-churn-app .`
	 - `docker run -p 8501:8501 ecommerce-churn-app`
3. Streamlit Cloud deployment:
	 - Repository connected to Streamlit Cloud, using `app/streamlit_app.py` as
		 the entry point.

---

## 4. Troubleshooting Guide

### 4.1 Common Issues

**Issue 1: FileNotFoundError for processed data or models**

- **Symptom:** Errors like `X_train.csv not found` or `best_model.pkl not
	found`.
- **Cause:** The data pipeline scripts have not been executed in the correct
	order, or paths differ from expectations.
- **Fix:**
	- Run the pipeline from the project root:
		- `python src/01_data_acquisition.py`
		- `python src/02_data_cleaning.py`
		- `python src/03_feature_engineering.py`
		- `python src/04_model_preparation.py`
	- Ensure you run commands with the working directory set to the repository
		root.

**Issue 2: Path issues inside Streamlit pages**

- **Symptom:** Streamlit dashboard cannot find `X_test.csv` or evaluation
	plots.
- **Cause:** Relative paths are resolved from the `app/pages` directory.
- **Fix:**
	- Use `os.path.dirname(os.path.dirname(os.path.dirname(__file__)))` to get
		the project root.
	- Build paths relative to that root (as implemented in
		`app/pages/04_Model_Dashboard.py`).

**Issue 3: Dependency or version conflicts (especially in Docker/Cloud)**

- **Symptom:** Import errors, incompatible versions, or failures on
	Streamlit Cloud.
- **Cause:** Package versions not pinned or environment not matching
	`requirements.txt`.
- **Fix:**
	- Always install from `requirements.txt`.
	- If using Docker, rebuild the image after changing dependencies.
	- For Streamlit Cloud, ensure `requirements.txt` is in the repo root and
		matches local development versions.

**Issue 4: Model or scaler mismatch**

- **Symptom:** Shape or feature alignment errors when calling `predict`.
- **Cause:** Model trained on one set/order of features while
	`app/predict.py` uses a different schema.
- **Fix:**
	- Regenerate `feature_names.json`, `scaler.pkl`, and `best_model.pkl`
		together by rerunning the pipeline and model training notebooks.
	- Ensure `preprocess_input` relies on `feature_names.json` to add missing
		columns and order them correctly.

---

## 5. Version Control and Reproducibility

- The project is tracked in Git and hosted on GitHub:
	- Repository: `https://github.com/JallaShalini/ecommerce-churn-prediction`
- Key practices:
	- Scripts and notebooks use relative paths based on the project root.
	- All important artifacts (cleaning stats, feature info, evaluation plots,
		trained models) are saved under `data/processed/`, `models/`, and
		`visualizations/`.
	- `submission.json` documents the final model choice, deployment platform,
		and student information.

This technical documentation, together with the notebooks and scripts, should
be sufficient for another engineer to reproduce the full pipeline and redeploy
the model.