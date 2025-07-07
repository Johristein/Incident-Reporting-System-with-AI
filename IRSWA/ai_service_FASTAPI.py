from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
tfidf_vectorizer = joblib.load("models/tfidf_vectorizer.joblib")
rf_classifier = joblib.load("models/rf_classifier.joblib")
xgb_classifier = joblib.load("models/xgb_classifier.joblib")
lr_classifier = joblib.load("models/lr_classifier.joblib")
ann_model = load_model("models/ann_model.h5")
label_encoder = joblib.load("models/label_encoder.joblib")

# Request schema
class IncidentLog(BaseModel):
    message: str
    model: str = "rf" 

# Get combined SBERT + TF-IDF features
def get_combined_features(text: str):
    sbert_vec = sbert_model.encode([text])  
    tfidf_vec = tfidf_vectorizer.transform([text]).toarray()  
    combined = np.hstack((sbert_vec, tfidf_vec))  
    return combined

# Severity logic
def assign_severity(label):
    label = label.lower()
    if "ddos" in label or "dos" in label:
        return "high"
    elif "injection" in label or "xss" in label:
        return "medium"
    elif "brute" in label or "scan" in label:
        return "low"
    else:
        return "unknown"

@app.post("/analyze")
def analyze(log: IncidentLog):
    try:
        emb = get_combined_features(log.message)
        model_choice = log.model.lower()

        if model_choice == "rf":
            prediction = rf_classifier.predict(emb)[0]
        elif model_choice == "xgb":
            prediction = xgb_classifier.predict(emb)[0]
        elif model_choice == "lr":
            prediction = lr_classifier.predict(emb)[0]
        elif model_choice == "ann":
            prediction = np.argmax(ann_model.predict(emb), axis=1)[0]
        else:
            raise HTTPException(status_code=400, detail="Invalid model")

        label = label_encoder.inverse_transform([prediction])[0]
        severity = assign_severity(label)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "model_used": model_choice.upper(),
            "attack_type": label,
            "severity": severity,
            "status": "logged",
            "timestamp": timestamp
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
