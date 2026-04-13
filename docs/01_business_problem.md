# Business Problem

E-commerce companies often face customer churn, where customers stop purchasing from the platform.

Customer churn results in revenue loss and increased marketing costs required to acquire new customers.

In this project, **churn is defined as a previously active customer who makes no purchase in the 90 days following a reference date**. The model therefore predicts the probability that a currently active customer will become inactive for at least the next 90 days.

The goal of this project is to build a machine learning system that predicts whether a customer is likely to churn in this 90-day horizon based on their historical purchase behavior.

By predicting churn early, businesses can take proactive actions such as personalized offers, loyalty programs, and targeted marketing campaigns focused on high‑risk customers.

Model performance will later be evaluated using ROC-AUC, Precision, Recall, and F1 score on the churn class, with explicit minimum/target/stretch thresholds defined in 04_success_criteria.md. These metrics will be reported consistently in 11_model_selection.md and submission.json.