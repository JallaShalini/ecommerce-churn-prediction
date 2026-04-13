# Project Scope

The scope of this project includes:

- Defining customer churn as **no purchase in the 90 days after a reference date** and translating this into a supervised learning target
- Building a machine learning model to predict the probability that an active customer will churn in the next 90 days
- Performing exploratory data analysis on transaction data
- Creating customer behavior features at the customer level using a temporal split (history window for features, future 90-day window for churn label)
- Training and comparing multiple machine learning models
- Selecting the best model based on ROC-AUC, Precision, Recall, and F1 on the churn class
- Deploying a prediction application using Streamlit

The system supports both:

1. Single customer prediction via a web interface
2. Batch prediction using CSV files uploaded to the application

All reported metrics and definitions in this scope are aligned with 04_success_criteria.md and will be reused consistently in 11_model_selection.md and submission.json.