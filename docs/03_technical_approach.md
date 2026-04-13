# Technical Approach

The project follows a structured machine learning workflow:

1. Data Collection
2. Data Cleaning
3. Feature Engineering
4. Exploratory Data Analysis
5. Model Training
6. Model Evaluation
7. Model Deployment

To avoid data leakage and to respect the business definition of churn, feature engineering and label creation are done using a **temporal split**:

- A historical window of transactions is used to compute customer-level features.
- A subsequent 90-day window is used to determine whether each previously active customer churned (no purchases in that window).
- This setup makes the target "will the customer make any purchase in the next 90 days?" consistent with the business definition in 01_business_problem.md and the scope in 02_project_scope.md.

The models tested include:

- Logistic Regression
- Decision Tree
- Random Forest
- Neural Network
- XGBoost

Models are evaluated on ROC-AUC, Precision, Recall, and F1 score for the churn class using a held-out test set. The minimum/target/stretch thresholds for these metrics are defined in 04_success_criteria.md.

The best performing model that meets or exceeds the minimum success thresholds is saved and used for prediction in the deployed Streamlit application.