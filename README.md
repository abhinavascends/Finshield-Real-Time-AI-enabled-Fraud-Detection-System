# FinShield
### AI-Enabled Real-Time Transaction Fraud Detection System

FinShield is an end-to-end transaction risk detection system designed to
identify anomalous financial activity and expose fraud-risk scores through
an API-driven architecture.

The system combines transaction-level feature engineering, unsupervised
anomaly detection, supervised classification, model serialization,
ONNX-based inference, persistent transaction storage, authentication,
and a React monitoring interface.

---

## 1. System Objective

Financial transactions can exhibit suspicious behavior through unusual
amounts, transaction frequency, timing, location changes, account activity,
and other behavioral signals.

FinShield approaches the problem as a multi-stage ML and backend pipeline:

```text
Transaction
     │
     ▼
Feature Engineering
     │
     ├── Numerical Features
     ├── Categorical Features
     ├── Temporal Features
     └── User Behaviour Features
     │
     ▼
Preprocessing
     │
     ├── Standard Scaling
     └── One-Hot Encoding
     │
     ▼
Anomaly Detection
     │
     └── Isolation Forest
     │
     ▼
Fraud Classification
     │
     └── XGBoost
     │
     ▼
Risk / Fraud Score
     │
     ├── API Response
     ├── PostgreSQL
     └── Alert Pipeline
     │
     ▼
React Monitoring Dashboard
```

---

# 2. Core Capabilities

### Transaction Risk Scoring

Transactions can be submitted to the backend and evaluated by the
machine-learning inference pipeline.

### Behavioural Feature Engineering

The feature pipeline incorporates transaction history and behavioural
signals such as:

- Transaction frequency
- Average transaction amount
- Deviation from historical average
- Transaction hour
- Day of week
- Account balance
- Login attempts
- Primary user location
- Unusual-location indicator

### Anomaly Detection

Isolation Forest is used to identify transactions whose feature patterns
differ significantly from the learned distribution of normal activity.

### Fraud Classification

XGBoost is used as the supervised classification layer after feature
preparation and anomaly-derived labeling.

### Persistent Transaction Storage

PostgreSQL stores transaction records, fraud status and risk-related
information.

### Alert Infrastructure

Redis is used as the supporting infrastructure for transaction/alert
messaging and low-latency access patterns.

### Authentication

JWT-based authentication protects authenticated API operations.

### Web Dashboard

A React frontend provides transaction scoring and transaction-history
visualization.

---

# 3. Machine Learning Pipeline

## 3.1 Input Data

The project works with transaction-level banking data containing numerical
and categorical attributes.

The feature set includes signals such as:

```text
TransactionAmount
CustomerAge
TransactionDuration
LoginAttempts
AccountBalance
user_transaction_count
user_avg_transaction_amount
deviation_from_user_avg
transaction_hour
transaction_day_of_week
TransactionType
Location
Channel
CustomerOccupation
user_primary_location
is_unusual_location
```

---

## 3.2 Numerical Feature Processing

Numerical features are standardized using:

```text
StandardScaler
```

This prevents features with larger numerical ranges from dominating the
distance-based/anomaly detection process.

---

## 3.3 Categorical Feature Processing

Categorical attributes are converted into numerical representations using:

```text
OneHotEncoder
```

The encoder is configured to tolerate previously unseen categories during
inference.

---

## 3.4 Feature Matrix

After preprocessing:

```text
Scaled Numerical Features
          +
One-Hot Encoded Categorical Features
          │
          ▼
     Combined Feature Matrix
```

The resulting matrix is used as the common representation for the
machine-learning pipeline.

---

# 4. Anomaly Detection Layer

The first detection stage uses:

```text
Isolation Forest
```

Isolation Forest is useful when explicit fraud labels are unavailable or
insufficient because it learns the structure of the feature distribution
and identifies observations that are easier to isolate from the majority
of transactions.

Current model configuration includes:

```text
n_estimators = 100
contamination = 0.01
random_state = 42
```

The anomaly score is derived from the Isolation Forest decision function.

A threshold is then applied to identify transactions considered anomalous.

---

# 5. Supervised Classification Layer

Following anomaly detection, the resulting fraud indicator is used to
construct the classification target for the current training pipeline.

The project then trains:

```text
XGBoost Classifier
```

The training pipeline performs:

```text
Feature Matrix
      │
      ▼
Train / Test Split
      │
      ▼
Class Distribution Analysis
      │
      ▼
scale_pos_weight
      │
      ▼
XGBoost Training
      │
      ├── Class Prediction
      └── Fraud Probability
```

The use of `scale_pos_weight` addresses the imbalance between the
majority and minority classes during classifier training.

---

# 6. Model Evaluation

The classification pipeline evaluates the trained model using:

- Classification report
- ROC-AUC
- ROC curve
- Predicted class
- Predicted probability

The ROC curve is generated from the model's predicted fraud probabilities.

This allows the model to be evaluated beyond a single classification
threshold.

---

# 7. Model Persistence

The trained components are serialized so that model training and inference
can remain separate.

Important artifacts include:

```text
iso_forest_model.pkl
onehot_encoder.pkl
xgb_model.pkl
```

The project also contains an ONNX inference artifact:

```text
fraud_detector_1bit.onnx
```

This provides a path toward deployment-oriented inference without requiring
the complete training environment during serving.

---

# 8. ONNX Inference Pipeline

The XGBoost model can be converted into ONNX format.

```text
Trained XGBoost Model
        │
        ▼
ONNX Conversion
        │
        ▼
fraud_detector.onnx
        │
        ▼
Quantization
        │
        ▼
fraud_detector_1bit.onnx
```

The quantization stage uses ONNX Runtime's dynamic quantization utilities.

This separates the training representation from the deployment-oriented
model representation.

---

# 9. Backend Architecture

The backend is implemented using:

```text
Python
FastAPI
PostgreSQL
Redis
JWT
ONNX Runtime
```

The backend is responsible for:

1. Receiving transaction requests
2. Validating incoming data
3. Running model inference
4. Producing a fraud/risk result
5. Persisting transaction information
6. Generating high-risk alerts
7. Supporting authenticated operations
8. Providing API access to the frontend

---

# 10. API Layer

The backend exposes transaction-oriented endpoints.

### Transaction Scoring

```http
POST /transactions/score
```

Used to submit a transaction for model evaluation.

Conceptually:

```text
Client
  │
  │ POST transaction
  ▼
FastAPI
  │
  ▼
Feature / Model Inference
  │
  ▼
Risk Score
  │
  ├── Fraud Decision
  └── Persistence / Alert
  │
  ▼
JSON Response
```

### Transaction Ingestion

```http
POST /transactions/ingest
```

The ingestion path provides a mechanism for accepting transaction events
and placing them into Redis-backed processing infrastructure.

### Alert Stream

```http
WebSocket /ws/alerts
```

The backend contains a WebSocket-based alert path for delivering
high-risk events through Redis-backed messaging.

---

# 11. Authentication

Authentication is implemented using:

```text
JWT
```

The authentication layer:

- Creates signed access tokens
- Applies token expiration
- Extracts authenticated users
- Rejects invalid authentication credentials

The secret key is supplied through environment configuration rather than
being hard-coded into the application.

---

# 12. PostgreSQL Data Layer

The persistence layer uses PostgreSQL.

The database schema contains two primary entities:

```text
transactions
      │
      └── Transaction records

alerts
      │
      └── High-risk transaction events
```

### Transactions

Stores information associated with evaluated transactions, including:

- Account identifier
- Transaction amount
- Location
- Event timestamp
- Fraud status
- Fraud/risk probability

### Alerts

Stores high-risk events associated with transactions.

This creates a separation between the transaction history and the alert
stream.

---

# 13. Redis Integration

Redis is used as the low-latency messaging layer.

The current architecture provides support for:

```text
Transaction events
      │
      ▼
Redis Streams

High-risk events
      │
      ▼
Redis alert channel / stream
      │
      ▼
WebSocket clients
```

This provides the foundation for moving from a simple request-response
architecture toward event-driven transaction processing.

---

# 14. Frontend

The monitoring interface is implemented using:

```text
React
Axios
CSS
```

The frontend contains two primary workflows.

### Transaction Scoring

A transaction can be entered through the scoring interface and submitted
to the FastAPI backend.

The response is then displayed to the user.

### Transaction Monitoring

The dashboard displays transaction history with information such as:

```text
Transaction ID
Account ID
Amount
Location
Event Time
Fraud Status
Risk / Fraud Score
```

High-risk transactions are surfaced as alerts in the dashboard.

---

# 15. Repository Structure

```text
FinShield/
│
├── app/
│   ├── main.py
│   ├── api.py
│   ├── auth.py
│   ├── db.py
│   │
│   ├── model/
│   │   ├── train_model.py
│   │   ├── convert_xgboost_to_onnx.py
│   │   └── quantize_onnx_model.py
│   │
│   └── Database/
│       └── schema.sql
│
├── model/
│   ├── train_model.py
│   ├── convert_xgboost_to_onnx.py
│   └── quantize_onnx_model.py
│
├── frontend/
│   ├── src/
│   │   ├── Dashboard.jsx
│   │   ├── TransactionScore.js
│   │   └── components/
│   │
│   └── package.json
│
├── tests/
│   └── test_main.py
│
├── Database/
│   └── schema.sql
│
├── bank_transactions_featured.csv
├── Feature_Generation.py
├── isolationforest.py
├── IsolationForest.ipynb
│
├── iso_forest_model.pkl
├── onehot_encoder.pkl
├── xgb_model.pkl
│
├── generate_token.py
├── run.py
├── requirements.txt
└── README.md
```

---

# 16. Technology Stack

| Layer | Technologies |
|---|---|
| Language | Python, JavaScript |
| ML | Scikit-learn, XGBoost |
| Data Processing | Pandas, NumPy |
| Feature Processing | StandardScaler, OneHotEncoder |
| Anomaly Detection | Isolation Forest |
| Model Deployment | ONNX, ONNX Runtime |
| Backend | FastAPI |
| Authentication | JWT |
| Database | PostgreSQL |
| Messaging / Cache | Redis |
| Frontend | React |
| HTTP Client | Axios |
| Testing | Pytest, React Testing Library |
| Version Control | Git, GitHub |

---

# 17. Local Development

## Requirements

Install the following before running the project:

```text
Python 3.8+
Node.js
npm
PostgreSQL
Redis
```

---

## Backend Setup

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd FinShield
```

Create a Python environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create the required environment variables:

```env
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<database>
JWT_SECRET=<your-secret>
```

Do not commit credentials or secrets to the repository.

---

## Database Setup

Create a PostgreSQL database and apply:

```text
Database/schema.sql
```

The schema initializes the transaction and alert tables.

---

## Run the Backend

From the backend/application directory:

```bash
uvicorn main:app --reload
```

The development API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 18. Frontend Setup

Move into the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm start
```

The development interface runs on:

```text
http://localhost:3000
```

---

# 19. Model Training

The training pipeline is implemented in:

```text
model/train_model.py
```

The high-level workflow is:

```text
Load Dataset
     │
     ▼
Remove Identifier / Non-model Columns
     │
     ▼
Separate Numerical + Categorical Features
     │
     ▼
StandardScaler
     │
     +
OneHotEncoder
     │
     ▼
Combined Feature Matrix
     │
     ▼
Isolation Forest
     │
     ▼
Anomaly-derived Fraud Indicator
     │
     ▼
Train/Test Split
     │
     ▼
XGBoost
     │
     ▼
Evaluation
     │
     ▼
Serialized Model Artifacts
```

Before running the training scripts, update dataset and artifact paths
to match the local environment.

---

# 20. Engineering Considerations

The project is being developed as a modular ML application rather than
as a standalone notebook.

The architecture separates:

```text
Data Preparation
       ↓
Feature Engineering
       ↓
Model Training
       ↓
Model Serialization
       ↓
Inference
       ↓
API Layer
       ↓
Persistence
       ↓
Frontend
```

This separation makes individual components easier to test, replace,
and optimize independently.

---

# 21. Development Roadmap

The system is being developed incrementally across several engineering
layers.

### Phase 1 — Data & Feature Pipeline

- Dataset preparation
- Numerical feature processing
- Categorical encoding
- Behavioural features
- Temporal features
- Location-based anomaly features
- Unified feature matrix

### Phase 2 — Anomaly Detection

- Isolation Forest
- Anomaly threshold selection
- Model persistence
- Inference validation

### Phase 3 — Supervised Classification

- Fraud labels
- Train/test split
- Imbalance handling
- XGBoost training
- Probability-based predictions
- Evaluation metrics

### Phase 4 — Model Deployment

- ONNX conversion
- Quantized model
- Inference validation
- Deployment-oriented model artifacts

### Phase 5 — Backend

- Transaction ingestion
- Fraud scoring API
- Authentication
- Database persistence
- Redis integration
- Alert processing

### Phase 6 — Frontend

- Transaction scoring interface
- Transaction history
- Risk visualization
- Fraud alerts
- Backend integration

### Phase 7 — Testing & Hardening

- API tests
- Model inference tests
- Integration tests
- Input validation
- Error handling
- Configuration cleanup
- Deployment preparation

---

# 22. Design Philosophy

FinShield is structured around one principle:

> Separate the intelligence layer from the application layer.

The machine-learning pipeline is responsible for identifying transaction
patterns and producing risk signals.

The backend is responsible for serving those signals reliably.

The database is responsible for persistence.

Redis provides the low-latency event infrastructure.

The frontend provides the operational interface.

This separation allows each layer to evolve independently while keeping
the complete transaction-to-decision pipeline observable.

---

## Status

**Active Development**

The project is being developed incrementally from the feature-engineering
layer through model training, inference optimization, backend integration,
persistent storage, frontend monitoring, and testing.
