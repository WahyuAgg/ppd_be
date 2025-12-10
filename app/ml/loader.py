import pickle
import numpy as np
from scipy.sparse import hstack

vec_raw = pickle.load(open("model/vec_raw.pkl", "rb"))
vec_clean = pickle.load(open("model/vec_clean.pkl", "rb"))
scaler = pickle.load(open("model/scaler.pkl", "rb"))
model = pickle.load(open("model/model.pkl", "rb"))
label_encoder = pickle.load(open("model/label_encoder.pkl", "rb"))

def predict_text(raw: str):
    from app.ml.preprocess import clean_text, extract_numeric_features

    clean = clean_text(raw)

    tf_raw = vec_raw.transform([raw])
    tf_clean = vec_clean.transform([clean])

    numeric = extract_numeric_features(raw)
    numeric_scaled = scaler.transform(numeric)

    X = hstack([tf_clean, numeric_scaled, tf_raw])

    pred = model.predict(X)
    label = label_encoder.inverse_transform(pred)[0]
    return label
