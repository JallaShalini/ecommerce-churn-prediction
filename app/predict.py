import json
import os
import pickle
from typing import Any, Dict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "data", "processed", "feature_names.json")


def load_model():
    """Load the trained best model for churn prediction."""
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def load_scaler():
    """Load the feature scaler used during training."""
    with open(SCALER_PATH, "rb") as f:
        return pickle.load(f)


def load_feature_names():
    """Load the ordered list of feature names expected by the model."""
    with open(FEATURES_PATH, "r") as f:
        return json.load(f)


def preprocess_input(data: Dict[str, Any]):
    """Preprocess a single customer input into the model-ready feature vector.

    This mirrors the steps in src/04_model_preparation.py:
    - Build a one-row DataFrame
    - One-hot encode CustomerSegment if present
    - Ensure all expected feature columns exist
    - Apply scaler to numeric columns
    - Reorder columns to match training feature order
    """

    import pandas as pd  # local import to avoid circular issues in Streamlit

    feature_names = load_feature_names()
    scaler = load_scaler()

    df = pd.DataFrame([data])

    # One-hot encode CustomerSegment consistently with training
    if "CustomerSegment" in df.columns:
        seg_dummies = pd.get_dummies(df["CustomerSegment"], prefix="Segment")
        df = pd.concat([df.drop(columns=["CustomerSegment"]), seg_dummies], axis=1)

    # Ensure all expected columns exist
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0

    # Restrict to expected features only, in correct order
    df = df[feature_names]

    # Scale numeric columns using the same logic as in src/04_model_preparation.py
    numeric_cols = [
        c
        for c in df.select_dtypes(include=["int64", "float64"]).columns
        if not c.startswith("Segment_")
    ]

    if numeric_cols:
        df[numeric_cols] = scaler.transform(df[numeric_cols])

    return df


def predict(data: Dict[str, Any]) -> int:
    """Return churn prediction (0/1) for a single customer."""
    model = load_model()
    processed = preprocess_input(data)
    prediction = model.predict(processed)
    return int(prediction[0])


def predict_proba(data: Dict[str, Any]) -> float:
    """Return churn probability (0-1) for a single customer."""
    model = load_model()
    processed = preprocess_input(data)
    proba = model.predict_proba(processed)
    return float(proba[0][1])