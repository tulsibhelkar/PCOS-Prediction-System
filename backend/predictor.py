import os
import joblib
import pandas as pd

# ---------------- Load Model ---------------- #

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "hybrid_pcos_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ---------------- Feature Order ---------------- #

FEATURES = [
    "Age (yrs)",
    "Weight (Kg)",
    "Pregnant(Y/N)",
    "No. of abortions",
    "Weight gain(Y/N)",
    "hair growth(Y/N)",
    "Skin darkening (Y/N)",
    "Hair loss(Y/N)",
    "Pimples(Y/N)",
    "Fast food (Y/N)",
    "FSH/LH",
    "Follicle No. (L)",
    "Follicle No. (R)",
    "Cycle(R/I)",
    "Cycle length(days)"
]

# ---------------- Prediction Function ---------------- #

def predict_pcos(input_data):

    input_df = pd.DataFrame([input_data])

    input_df = input_df[FEATURES]

    input_scaled = scaler.transform(input_df)

    prediction = int(model.predict(input_scaled)[0])

    probability = float(model.predict_proba(input_scaled)[0][1])

    return prediction, probability