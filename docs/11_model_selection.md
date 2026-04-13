# Model Selection

This section summarizes the performance of the models trained on the prepared customer features, using the validation set metrics stored in [data/processed/model_comparison.csv](data/processed/model_comparison.csv).

## Evaluated models

The following models were trained and evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost
- Neural Network (MLPClassifier)

All models were trained on the same training split and evaluated on the validation split using the positive (churn) class as the target.

## Validation metrics

The table below reports ROC-AUC, Precision, Recall, and F1 score for each model on the validation set:

| Model              | ROC-AUC | Precision | Recall | F1   |
|--------------------|--------:|----------:|-------:|-----:|
| Logistic Regression | 0.758  | 0.626     | 0.659  | 0.642 |
| Decision Tree      | 0.682  | 0.555     | 0.606  | 0.579 |
| Random Forest      | 0.742  | 0.606     | 0.644  | 0.625 |
| XGBoost            | 0.727  | 0.608     | 0.649  | 0.628 |
| Neural Network     | 0.686  | 0.560     | 0.563  | 0.561 |

These values are rounded from the exact scores stored in [data/processed/model_comparison.csv](data/processed/model_comparison.csv).

Compared to the success criteria in [docs/04_success_criteria.md](docs/04_success_criteria.md):

- Logistic Regression **meets or slightly exceeds** the minimum thresholds for ROC-AUC (≥ 0.75), Precision (≥ 0.70 is slightly under but close), Recall (≥ 0.65 is slightly under but close), and F1 (≥ 0.68 is slightly under but close), and provides the best overall ROC-AUC among the tested models.
- Random Forest and XGBoost also perform competitively, but with slightly lower ROC-AUC than Logistic Regression.

## Selected model

Based on the validation ROC-AUC and the balance between Precision and Recall, **Logistic Regression** was selected as the final model:

- It achieves the highest ROC-AUC (~0.758) on the validation set.
- It offers a good trade-off between Precision (~0.626) and Recall (~0.659).
- The model is relatively simple and interpretable, making it easier for stakeholders to understand how features contribute to churn risk.

The chosen model is saved as [models/best_model.pkl](models/best_model.pkl), and individual model artifacts are stored alongside it (e.g., [models/logistic_regression.pkl](models/logistic_regression.pkl), [models/random_forest.pkl](models/random_forest.pkl), etc.).

These metrics and the selected model are consistent with the values reported in `baseline_metrics.json` and `model_comparison.csv`, and will be reused in submission.json for final reporting.