## 🛡️ Incident Reporting System (IRS) with AI

> 📦 This project showcases a hybrid AI-powered incident analysis system built with **FastAPI**, integrating **SBERT**, **TF-IDF**, and multiple classifiers to automate detection of security incidents.

---

### 📁 Folder Structure

```
IRSWA/
├── models/                 # Contains all trained model files (.joblib, .h5)
├── ai_service_FASTAPI.py   # FastAPI backend
├── IRSINTER.html           # Simple frontend UI
├── airs_report.py          # Incident object, export logic
├── IRSWA.ipynb             # Training pipeline for all models
└── Incident_dataset.csv    # Input dataset for training
```

---

### 🤖 AI Models Integrated

All models are trained on **SBERT + TF-IDF** feature concatenation:

* `RandomForestClassifier`
* `XGBoostClassifier`
* `LogisticRegression`
* `Artificial Neural Network (ANN)`

Each model predicts the **attack type**, which is mapped to a severity level:

| Attack Type   | Severity |
| ------------- | -------- |
| SQL Injection | Medium   |
| XSS           | Medium   |
| DDoS / DoS    | High     |
| Port Scan     | Low      |
| Brute Force   | Low      |
| Unknown       | Unknown  |

---

### 🧠 Feature Engineering

* **SBERT:** SentenceTransformer `all-MiniLM-L6-v2`
* **TF-IDF:** 200 features, trained and serialized
* Combined: 384 (SBERT) + 200 (TF-IDF) = 584 features total

---

### 🧪 Training Pipeline (`train_model.py`)

1. Load & preprocess dataset
2. Generate SBERT embeddings
3. Extract TF-IDF features
4. Concatenate features
5. Train all 4 models
6. Save to `models/` directory

---

### 🌐 FastAPI Backend (`app.py`)

**Endpoint:** `/analyze`

**Request:**

```json
{
  "message": "SQL injection attempt on login form",
  "model": "xgb"
}
```

**Response:**

```json
{
  "model_used": "XGB",
  "attack_type": "SQL Injection",
  "severity": "medium",
  "status": "logged",
  "timestamp": "2025-07-07 17:00:00"
}
```

---

### 💻 Interface (`interface.html`)

* Input attack message
* Select model: ANN, RF, XGB, Logistic
* Shows prediction and allows CSV/JSON download

---

### 📤 Logging (`ai_logic.py`)

* Saves predictions to:

  * `logs/incidents_YYYY-MM-DD.csv`
  * `logs/incidents_YYYY-MM-DD.json`
* Triggers alerts if severity is **High** or type is **Unknown**

---

### 🚀 How to Run It

#### 1. Clone and Setup

```bash
git clone [github](https://github.com/Johristein/Incident-Reporting-System-with-AI.git
cd IRSWA
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Run FastAPI Server

```bash
uvicorn app:app --reload
```

#### 3. Open UI

Go to `IRSINTER.html` in your browser (open directly or via live server)

---

### 📝 Dependencies

```txt
fastapi
pydantic
sentence-transformers
scikit-learn
xgboost
joblib
tensorflow
numpy
pandas
uvicorn
```

---


### 📣 Purpose

> 🛡️ This IRS project demonstrates how hybrid AI methods can automate the classification, logging, and alerting of cybersecurity incidents — applicable for educational labs, SOC prototypes, or real-time defense simulations.
