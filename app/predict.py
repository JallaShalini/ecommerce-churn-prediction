import pandas as pd
import numpy as np
import pickle
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "data", "processed", "feature_names.json")


def load_model():
    return pickle.load(open(MODEL_PATH, "rb"))


def load_features():
    return json.load(open(FEATURE_PATH))


def preprocess_input(data):

    feature_names = load_features()

    df = pd.DataFrame([data])

    # Encode categorical columns
    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        df[col] = df[col].astype("category").cat.codes

    # Add missing columns
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0

    # Reorder columns
    df = df[feature_names]

    return df


def predict(data):

    model = load_model()

    processed = preprocess_input(data)

    prediction = model.predict(processed)

    return int(prediction[0])


def predict_proba(data):

    model = load_model()

    processed = preprocess_input(data)

    prob = model.predict_proba(processed)

    return float(prob[0][1])