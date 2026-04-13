# Deployment Guide

## 1. Application Entry Point

- Streamlit app entry: `app/streamlit_app.py`

From the project root:

```bash
streamlit run app/streamlit_app.py
```

## 2. Requirements

The application depends on the following Python packages (see `requirements.txt`):

- streamlit>=1.32
- pandas>=2.1
- numpy>=1.26
- scikit-learn>=1.3
- joblib>=1.3
- plotly>=5.18
- openpyxl>=3.1
- xgboost==2.0.3
- scipy>=1.11

### Recommended Environment Setup

```bash
python -m venv venv
venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

## 3. Running the App Locally

From the project root:

1. Ensure the data pipeline has been run and that the following exist:
   - `data/processed/customer_features.csv`
   - `data/processed/X_test.csv`, `data/processed/y_test.csv`
   - `models/best_model.pkl`
   - `models/scaler.pkl`
   - `data/processed/feature_names.json`
   - Evaluation plots under `visualizations/evaluation/`.
2. Start Streamlit:

   ```bash
   streamlit run app/streamlit_app.py
   ```

3. Open the URL printed by Streamlit, typically:

   - Local URL: http://localhost:8501

## 4. Deployment URL

At the time of writing, the application is intended to run locally for grading.
If you deploy it (e.g., to Streamlit Community Cloud or another platform), use
this section to record the live URL:

- Deployed URL: _to be updated if/when hosted_

## 5. Docker-Based Deployment (Optional)

A `Dockerfile` and `docker-compose.yml` are included in the repository. A
simple workflow is:

```bash
docker build -t ecommerce-churn-app .
docker run -p 8501:8501 ecommerce-churn-app
```

Then access the app at:

- http://localhost:8501

Update this guide with any additional platform-specific steps if you deploy to
cloud infrastructure.
