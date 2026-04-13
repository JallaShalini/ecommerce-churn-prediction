# Churn Definition

In this project, **customer churn** is defined using a temporal split of the transaction history into a **training window** and a **future observation window**.

## Temporal split

- Let `max_date = df['InvoiceDate'].max()` be the most recent transaction date in the cleaned dataset.
- Define the **observation window end** as:
	- `observation_end = max_date`
- Define the **training cutoff** as 90 days before the last date:
	- `training_cutoff = max_date - 90 days`
- All transactions with `InvoiceDate <= training_cutoff` belong to the **training period**.
- All transactions with `training_cutoff < InvoiceDate <= observation_end` belong to the **observation period**.

## Churn label

- **Training customers**: customers who make at least one purchase in the training period.
- **Observation customers**: customers who make at least one purchase in the observation period.
- For each customer who appears in the training period, we define:
	- `Churn = 1` (churned) if they **do not** appear in the observation period.
	- `Churn = 0` (active) if they **do** appear in the observation period.

In other words, a customer is considered **churned** if they were active during the training window but make **no purchases in the 90 days following the training cutoff**. This definition is implemented in the feature engineering pipeline in [src/03_feature_engineering.py](src/03_feature_engineering.py) and is used consistently throughout the project for model training and evaluation.