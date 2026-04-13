import os

import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

from predict import load_model

st.title("📈 Model Dashboard")

st.write("Test set performance of the deployed churn model.")

# app/pages -> app -> project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

X_test_path = os.path.join(BASE_DIR, "data", "processed", "X_test.csv")
y_test_path = os.path.join(BASE_DIR, "data", "processed", "y_test.csv")

model = load_model()
X_test = pd.read_csv(X_test_path)
y_test = pd.read_csv(y_test_path).iloc[:, 0]

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

roc_auc = roc_auc_score(y_test, y_prob)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)

metrics_df = pd.DataFrame(
	{
		"Metric": [
			"ROC-AUC",
			"Accuracy",
			"Precision",
			"Recall",
			"F1-score",
		],
		"Score": [
			roc_auc,
			accuracy,
			precision,
			recall,
			f1,
		],
	}
)

st.subheader("📊 Test Metrics")
st.table(metrics_df.style.format({"Score": "{:.3f}"}))

st.bar_chart(metrics_df.set_index("Metric"))

st.subheader("📉 Evaluation Plots")

viz_dir = os.path.join(BASE_DIR, "visualizations", "evaluation")

plots = [
	("ROC Curve", "roc_curve.png"),
	("Precision-Recall Curve", "precision_recall_curve.png"),
	("Confusion Matrix", "confusion_matrix.png"),
	("Prediction Probability Distribution", "prediction_distribution.png"),
	("Calibration Curve", "calibration_curve.png"),
]

for title, filename in plots:
	plot_path = os.path.join(viz_dir, filename)
	if os.path.exists(plot_path):
		st.markdown(f"#### {title}")
		st.image(plot_path, use_column_width=True)