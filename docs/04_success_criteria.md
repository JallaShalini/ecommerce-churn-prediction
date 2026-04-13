# Success Criteria

The project will be considered successful along two dimensions:

1. **Model performance** on predicting churn (no purchase in the next 90 days)
2. **Product readiness** of the deployed Streamlit application

## 1. Model performance criteria

We evaluate the model on the positive (churn) class using a held-out test set. The following metrics and thresholds define minimum, target, and stretch goals:

| Metric (churn class) | Minimum | Target | Stretch |
| --------------------- | ------- | ------ | ------- |
| ROC-AUC              | 0.75    | 0.80   | 0.85    |
| Precision            | 0.70    | 0.75   | 0.80    |
| Recall               | 0.65    | 0.70   | 0.75    |
| F1 score             | 0.68    | 0.72   | 0.78    |

- **Minimum**: The model must meet or exceed all minimum thresholds to be accepted.
- **Target**: The preferred operating point; models near or above these values are considered strong.
- **Stretch**: Aspirational performance indicating an excellent model.

These thresholds will be used consistently in 11_model_selection.md to compare candidate models and in submission.json to report final achieved metrics.

## 2. Product and deployment criteria

The project will also be considered successful from a product perspective if:

- The deployed Streamlit application starts without errors using the provided Docker configuration.
- Both single-customer and batch (CSV) prediction flows work end-to-end.
- Inputs are validated and user-friendly error messages are shown for invalid files or values.
- Model predictions (churn probability and label) are displayed clearly enough for a business user to act on.

Meeting the **minimum model performance thresholds** and all **product criteria** above constitutes overall project success.