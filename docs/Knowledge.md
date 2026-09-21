# AI-Powered Real-Time Fraud Detection System --- Project Knowledge

> Primary AI/coding-assistant context for the project. This combines the
> project knowledge previously maintained in Obsidian with the relevant
> structural information obtained from the actual codebase and Graphify
> analysis.

------------------------------------------------------------------------

## 1. Project Identity

**Project:** AI-Powered Real-Time Fraud Detection System

**Objective:** Build an end-to-end transaction fraud/anomaly detection
platform that accepts transaction data, engineers behavioral features,
performs ML-based anomaly/fraud detection, exposes scoring through
FastAPI, persists transaction/alert data, supports Redis-based alert
infrastructure, and provides a React monitoring/scoring interface.

The project should be understood as an application, not merely an ML
notebook.

Main layers:

1.  Data and feature engineering
2.  Anomaly detection
3.  Supervised classification
4.  Model evaluation
5.  ONNX inference/optimization
6.  FastAPI backend
7.  PostgreSQL persistence
8.  Redis alert infrastructure
9.  JWT authentication
10. React frontend
11. Testing and documentation

------------------------------------------------------------------------

## 2. Technology Stack

### Machine Learning

-   Python
-   Pandas
-   NumPy
-   scikit-learn
-   XGBoost
-   Joblib
-   ONNX
-   ONNX Runtime
-   onnxmltools
-   Matplotlib

### Backend

-   FastAPI
-   Uvicorn
-   Pydantic
-   PostgreSQL
-   psycopg2
-   Redis
-   python-jose
-   python-dotenv

### Frontend

-   React
-   React DOM
-   Axios
-   react-scripts / Create React App
-   Testing Library

### Testing

-   pytest
-   FastAPI TestClient

### Documentation / Project Intelligence

-   Obsidian
-   Graphify
-   Markdown

------------------------------------------------------------------------

## 3. Repository Structure

Known project structure:

``` text
AI-Powered-Real-Time-Fraud-Detection-System/
├── app/
│   ├── api.py
│   ├── auth.py
│   ├── db.py
│   ├── main.py
│   ├── fraud_detector_1bit.onnx
│   ├── Database/
│   │   └── schema.sql
│   └── model/
│       ├── convert_xgboost_to_onnx.py
│       ├── quantize_onnx_model.py
│       └── train_model.py
├── Database/
│   └── schema.sql
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── public/
│   └── src/
│       ├── App.js
│       ├── App.jsx
│       ├── Dashboard.jsx
│       ├── TransactionScore.js
│       ├── components/
│       │   ├── HistoryTable.jsx
│       │   ├── ScoreResult.jsx
│       │   └── TransactionScore.js
│       └── ...
├── model/
│   ├── convert_xgboost_to_onnx.py
│   ├── quantize_onnx_model.py
│   └── train_model.py
├── tests/
│   ├── test_main.py
│   └── Result/
├── bank_transactions_featured.csv
├── Feature_Generation.py
├── IsolationForest.ipynb
├── isolationforest.py
├── iso_forest_model.pkl
├── onehot_encoder.pkl
├── xgb_model.pkl
├── generate_token.py
├── pytest.ini
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

------------------------------------------------------------------------

## 4. High-Level Architecture

``` text
                    TRANSACTION SOURCE
                           |
                           v
                  +------------------+
                  | React Frontend   |
                  | Transaction Form |
                  +--------+---------+
                           |
                           | HTTP
                           v
                  +------------------+
                  |    FastAPI       |
                  | Validation/API   |
                  +--------+---------+
                           |
                           v
              +--------------------------+
              | Feature Preparation     |
              | Numeric + Categorical    |
              | Behavioral Features     |
              +------------+-------------+
                           |
                           v
                 +-------------------+
                 | ML Inference      |
                 | Isolation Forest  |
                 | XGBoost / ONNX    |
                 +---------+---------+
                           |
                     +-----+------+
                     |            |
                     v            v
              Fraud/Risk Score  Decision
                     |            |
                     +-----+------+
                           |
              +------------+-------------+
              |                          |
              v                          v
       PostgreSQL                    Redis
       Transactions                 Alerts/
       History                      Events/Cache
              |
              v
       React Dashboard
```

------------------------------------------------------------------------

## 5. End-to-End Transaction Flow

A transaction can contain:

``` text
account_id
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

Intended flow:

``` text
Input transaction
      ↓
Schema validation
      ↓
Feature preparation
      ↓
Numerical preprocessing
      ↓
Categorical encoding
      ↓
Combined feature vector
      ↓
ML inference
      ↓
Anomaly/fraud score
      ↓
Fraud decision
      ↓
Persistence
      ↓
Alert generation for high-risk cases
      ↓
API response
```

------------------------------------------------------------------------

## 6. Dataset

Primary dataset:

``` text
bank_transactions_featured.csv
```

Known numerical features:

-   TransactionAmount
-   CustomerAge
-   TransactionDuration
-   LoginAttempts
-   AccountBalance
-   user_transaction_count
-   user_avg_transaction_amount
-   deviation_from_user_avg
-   transaction_hour
-   transaction_day_of_week

Known categorical features:

-   TransactionType
-   Location
-   Channel
-   CustomerOccupation
-   user_primary_location
-   is_unusual_location

The training script also references source fields such as:

-   TransactionID
-   AccountID
-   TransactionDate
-   PreviousTransactionDate
-   DeviceID
-   IP Address
-   MerchantID

These are excluded from the model matrix in the current training
implementation.

------------------------------------------------------------------------

## 7. Feature Engineering

Feature engineering is a core part of the system.

### Transaction amount

`TransactionAmount`

Represents monetary transaction size.

### Customer age

`CustomerAge`

Provides demographic context.

### Transaction duration

`TransactionDuration`

Captures transaction timing behavior.

### Login attempts

`LoginAttempts`

Provides a security/behavioral signal.

### Account balance

`AccountBalance`

Provides financial context.

### User transaction count

`user_transaction_count`

Captures account activity level.

### User average transaction amount

`user_avg_transaction_amount`

Provides a customer-specific spending baseline.

### Deviation from user average

`deviation_from_user_avg`

Represents how far the current transaction differs from the user's
typical amount. The exact formula should follow the implementation
rather than being assumed.

### Temporal features

-   `transaction_hour`
-   `transaction_day_of_week`

These capture transaction timing patterns.

### Location behavior

-   `user_primary_location`
-   `is_unusual_location`

These capture whether transaction location behavior differs from the
user's normal pattern.

------------------------------------------------------------------------

## 8. Preprocessing

### Numerical preprocessing

The project uses:

``` python
StandardScaler()
```

to standardize numerical features.

### Categorical preprocessing

The project uses:

``` python
OneHotEncoder(
    handle_unknown='ignore',
    sparse_output=False
)
```

This transforms categorical fields into numeric binary features.

`handle_unknown='ignore'` is important at inference time because
production data may contain categories not observed during training.

### Final matrix

``` text
scaled numerical features
          +
one-hot categorical features
          ↓
combined model matrix
```

The matrix is converted to `float32` where required by inference.

------------------------------------------------------------------------

## 9. Isolation Forest

Isolation Forest is the unsupervised anomaly-detection component.

### Motivation

The initial fraud dataset did not provide a conventional trusted
`Is_Fraud` target, so Isolation Forest provides a way to identify
structurally unusual transactions without requiring manual fraud labels.

### Concept

Isolation Forest repeatedly partitions observations using randomized
trees. An unusual observation tends to become isolated with fewer
partitions.

``` text
easy to isolate
      ↓
more anomalous
```

### Current configuration

The code uses configurations including:

``` python
IsolationForest(
    n_estimators=100,
    contamination=0.01,
    random_state=42
)
```

The active source code should always be checked before changing
configuration.

### Anomaly score

The project uses:

``` python
scores = -iso.decision_function(X)
```

so larger values correspond to greater anomaly magnitude.

### Prediction

Isolation Forest produces:

``` text
1  = normal
-1 = anomaly
```

The application maps the anomaly result into the fraud decision.

### Artifacts

``` text
iso_forest_model.pkl
onehot_encoder.pkl
```

The encoder and model must remain compatible with the training feature
ordering.

------------------------------------------------------------------------

## 10. Supervised XGBoost

The project contains a supervised XGBoost stage.

Pipeline:

``` text
feature matrix
      ↓
Isolation Forest-derived labels
      ↓
train/test split
      ↓
class imbalance handling
      ↓
XGBoost
      ↓
probability prediction
      ↓
evaluation
```

### Important modeling fact

The current training code derives `is_fraud` labels from Isolation
Forest anomaly scores.

Therefore, unless independently labeled fraud data is introduced, the
project should **not** claim that XGBoost is trained on verified human
fraud labels.

### Train/test split

The current implementation uses:

``` python
train_test_split(
    ...,
    test_size=0.3,
    stratify=y,
    random_state=42
)
```

### Class imbalance

The current implementation calculates:

``` python
neg, pos = (y_train == 0).sum(), (y_train == 1).sum()
scale_pos_weight = neg / pos
```

and passes that ratio to XGBoost.

This gives the minority class additional consideration during training.

### Model artifact

``` text
xgb_model.pkl
```

------------------------------------------------------------------------

## 11. Model Evaluation

The project uses:

``` python
classification_report(...)
roc_auc_score(...)
roc_curve(...)
```

### Classification report

Provides:

-   precision
-   recall
-   F1-score
-   support

Fraud systems must balance recall against false positives because missed
fraud and excessive alerts both have operational costs.

### ROC-AUC

Measures discrimination across classification thresholds.

Only actual measured results should be reported.

### ROC curve

The training code generates a ROC curve from:

``` python
roc_curve(y_test, y_prob)
```

------------------------------------------------------------------------

## 12. ONNX Conversion and Optimization

The project includes:

``` text
model/convert_xgboost_to_onnx.py
```

which converts the trained XGBoost model to ONNX.

Pipeline:

``` text
XGBoost
   ↓
ONNX conversion
   ↓
portable inference representation
```

The project also contains:

``` text
model/quantize_onnx_model.py
```

for optimized ONNX inference.

### Important naming correction

The current quantization code uses:

``` python
QuantType.QUInt8
```

which is 8-bit unsigned integer quantization.

Therefore the artifact name:

``` text
fraud_detector_1bit.onnx
```

should not be described as literally "1-bit quantization" unless the
implementation is changed accordingly.

------------------------------------------------------------------------

## 13. FastAPI Backend

Main backend:

``` text
app/main.py
```

Additional API module:

``` text
app/api.py
```

The backend is intended to expose:

-   transaction ingestion,
-   fraud scoring,
-   alert handling,
-   persistence,
-   real-time infrastructure.

------------------------------------------------------------------------

## 14. Transaction Schema

The main transaction schema contains:

``` text
account_id
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

This schema must remain synchronized across:

``` text
frontend
Pydantic
feature preparation
model input
database
tests
```

------------------------------------------------------------------------

## 15. API Endpoints

### Ingestion

``` text
POST /transactions/ingest
```

Purpose:

1.  validate transaction,
2.  persist transaction information,
3.  return confirmation.

### Scoring

``` text
POST /transactions/score
```

Purpose:

``` text
transaction
   ↓
feature preparation
   ↓
encoding
   ↓
model inference
   ↓
fraud/anomaly result
```

Current code uses response concepts such as:

``` json
{
  "anomaly_score": 0.0,
  "is_fraud": false
}
```

However, some older frontend/test code expects:

``` text
score
fraud_probability
```

This contract must be standardized.

------------------------------------------------------------------------

## 16. PostgreSQL

The project has SQL schemas for:

``` text
transactions
alerts
```

Transaction storage is intended to contain:

-   transaction ID
-   account
-   amount
-   location
-   event time
-   fraud state
-   fraud/anomaly score
-   behavioral features

Alert storage is intended to contain:

-   alert ID
-   transaction reference
-   alert type
-   creation timestamp

The database schema and Python insertion queries must be kept
synchronized.

------------------------------------------------------------------------

## 17. Redis

Redis is intended for low-latency infrastructure.

Current concepts include:

``` text
transactions
alerts
user:<account>
```

Redis is used for:

-   event/stream handling,
-   latest-score caching,
-   alert/event publishing.

Redis is not intended to replace PostgreSQL as the permanent transaction
database.

------------------------------------------------------------------------

## 18. JWT Authentication

File:

``` text
app/auth.py
```

Uses JWT and FastAPI OAuth2 mechanisms.

Conceptual flow:

``` text
credentials
    ↓
JWT
    ↓
Authorization
    ↓
protected endpoint
```

Secret configuration must come from an environment variable such as:

``` text
JWT_SECRET
```

Never commit a real secret.

------------------------------------------------------------------------

## 19. React Frontend

Frontend root:

``` text
frontend/
```

Important components:

``` text
App.jsx
Dashboard.jsx
TransactionScore.js
HistoryTable.jsx
ScoreResult.jsx
```

### Main flow

``` text
User enters transaction
        ↓
React form
        ↓
Axios POST
        ↓
FastAPI
        ↓
ML score
        ↓
ScoreResult
```

### History

`HistoryTable.jsx` requests transaction history and displays fields such
as:

-   transaction ID
-   account ID
-   score
-   fraud state
-   event time

### Dashboard

`Dashboard.jsx` is intended to display:

-   recent transactions,
-   fraud status,
-   anomaly/risk score,
-   high-risk alerts.

------------------------------------------------------------------------

## 20. Known Frontend/API Inconsistencies

The current codebase contains inconsistencies that should be fixed
rather than hidden.

1.  Some frontend code uses:

    ``` text
    localhost:8000
    ```

    while other code uses:

    ``` text
    127.0.0.1:8000
    ```

2.  Backend response may use:

    ``` text
    anomaly_score
    ```

    while components may expect:

    ``` text
    score
    ```

3.  Some older code expects:

    ``` text
    fraud_probability
    ```

4.  Database fields and Python insertion queries have not always been
    identical.

5.  `Dashboard.jsx` calls:

    ``` text
    /transactions/history
    ```

    but the inspected backend did not clearly contain a finalized
    matching endpoint.

6.  The test file contains old merge-conflict/incompatible API-contract
    material.

These are legitimate engineering fixes.

------------------------------------------------------------------------

## 21. Tests

Testing files:

``` text
tests/test_main.py
pytest.ini
```

The intended test coverage includes:

-   transaction ingestion,
-   transaction scoring,
-   fraud decision response.

A stronger final suite should also cover:

-   invalid input,
-   response schema,
-   model inference,
-   history endpoint,
-   persistence behavior where practical.

------------------------------------------------------------------------

## 22. Configuration

Expected environment variables include:

``` text
DATABASE_URL
REDIS_URL
JWT_SECRET
MODEL_PATH
```

Use:

``` text
.env
```

locally and keep it out of Git.

Recommended repository file:

``` text
.env.example
```

containing variable names but no secrets.

Avoid hardcoded machine paths such as:

``` text
/Users/mac/Desktop/...
/content/drive/MyDrive/...
```

Use project-relative paths or environment configuration.

------------------------------------------------------------------------

## 23. Run Commands

### Backend

``` bash
python -m venv .venv
```

Windows:

``` powershell
.venv\Scriptsctivate
```

Install:

``` bash
pip install -r requirements.txt
```

Run:

``` bash
uvicorn app.main:app --reload
```

Docs:

``` text
http://127.0.0.1:8000/docs
```

### Frontend

``` bash
cd frontend
npm install
npm start
```

Typical URL:

``` text
http://localhost:3000
```

### Tests

``` bash
pytest
```

------------------------------------------------------------------------

## 24. Graphify Context

The project was analyzed using Graphify.

Known Graphify output:

``` text
graphify-out/
├── GRAPH_REPORT.md
├── graph.json
├── manifest.json
├── .graphify_analysis.json
├── .graphify_labels.json
├── .graphify_labels.json.sig
└── cache/
```

`GRAPH_REPORT.md` contains structural analysis including communities,
cohesion, knowledge gaps, and suggested questions.

The visible analysis identified communities around:

-   React/frontend code,
-   `api.py`,
-   `index.js`,
-   frontend dependencies,
-   manifest-related frontend files.

The report also identified isolated/weakly connected nodes and
architectural knowledge gaps.

`manifest.json` records source-file metadata including:

-   modification time,
-   seen time,
-   AST hash,
-   semantic hash.

Graphify is a project-intelligence/analysis layer, not a runtime
dependency of the fraud detector.

Keep `graphify-out/` if it is useful for future AI-assisted development.

------------------------------------------------------------------------

## 25. Obsidian / AI Knowledge Usage

This file is intended to replace the deleted consolidated Obsidian
knowledge file as a single AI context document.

For future Claude/Copilot/other AI sessions:

1.  Provide this file as project context.
2.  Then provide the relevant source file(s).
3.  Ask the AI to inspect the current implementation before changing it.
4.  Treat source code as authoritative if this document disagrees with
    implementation.
5.  Keep architectural changes synchronized with frontend, backend,
    database, tests, and model contracts.

------------------------------------------------------------------------

## 26. AI Coding Rules

### Rule 1 --- Inspect first

Never assume an older implementation still exists.

### Rule 2 --- Preserve the architecture

``` text
Frontend
   ↓
FastAPI
   ↓
Feature preparation
   ↓
ML inference
   ↓
Persistence / alerts
```

### Rule 3 --- Keep contracts synchronized

Any transaction-field change must be checked across:

``` text
frontend payload
Pydantic schema
feature preparation
model input
database
tests
README
```

### Rule 4 --- No hardcoded machine paths

Use project-relative paths or environment variables.

### Rule 5 --- No secrets

Never commit:

-   `.env`
-   JWT secrets
-   database passwords
-   Redis credentials
-   API keys

### Rule 6 --- Do not silently change model behavior

Changes to:

-   feature ordering,
-   scaler,
-   encoder,
-   threshold,
-   model,
-   artifact

must be explicit.

### Rule 7 --- Do not invent metrics

Only report experimentally measured results.

### Rule 8 --- Test after meaningful changes

Run the relevant tests after backend/model/API modifications.

------------------------------------------------------------------------

## 27. Current Technical Debt

### High priority

-   Remove unresolved merge conflict markers.
-   Remove hardcoded local filesystem paths.
-   Synchronize API schemas.
-   Synchronize database schema with Python queries.
-   Implement/verify `/transactions/history`.
-   Standardize response field names.
-   Ensure inference preprocessing exactly matches training
    preprocessing.
-   Make model path configurable.
-   Remove secrets from source.
-   Clean authentication.
-   Repair/update tests.

### Medium priority

-   Add `.env.example`.
-   Add centralized configuration.
-   Add structured logging.
-   Add stronger input validation.
-   Add model/version metadata.
-   Improve artifact organization.
-   Add reproducible training instructions.

### Documentation priority

-   Clearly explain anomaly detection vs supervised classification.
-   Explain that XGBoost labels are derived from the anomaly pipeline if
    that remains true.
-   Document actual measured metrics.
-   Document API request/response schemas.
-   Document architecture.

------------------------------------------------------------------------

## 28. Recommended Engineering Sequence

The project can be developed incrementally through these logical stages:

``` text
01 Project foundation
02 Dependencies/environment
03 Git ignore/development config
04 Initial documentation
05 Dataset
06 Numerical features
07 Categorical features
08 User behavior features
09 Temporal features
10 Location anomaly feature
11 Final feature pipeline
12 Scaling
13 Encoding
14 Combined feature matrix
15 Isolation Forest
16 Anomaly threshold
17 Model artifacts
18 Isolation Forest tests
19 Supervised labels
20 Train/test split
21 Class imbalance
22 XGBoost
23 Model persistence
24 Probability inference
25 Classification metrics
26 ROC-AUC
27 Evaluation report
28 ONNX conversion
29 ONNX optimization
30 API schema
31 Ingestion API
32 Scoring API
33 PostgreSQL
34 Redis
35 Authentication
36 React dashboard
37 Integration tests + final documentation
```

This sequence is a development roadmap, not a claim that every stage
already exists independently in the current source.

------------------------------------------------------------------------

## 29. Interview-Level Technical Explanation

A concise explanation:

> I built an end-to-end fraud detection platform that combines
> behavioral feature engineering with anomaly detection and supervised
> classification. Transaction data is transformed using numerical
> scaling and categorical encoding, with customer-level behavioral
> signals such as transaction frequency, average amount deviation,
> temporal behavior, and location behavior. Isolation Forest provides an
> unsupervised anomaly-detection stage, and its derived labels are used
> in the current supervised XGBoost pipeline. The model can be converted
> to ONNX for deployment-oriented inference. FastAPI exposes transaction
> ingestion and scoring, PostgreSQL provides persistence, Redis supports
> low-latency alert infrastructure, and a React dashboard provides
> transaction scoring and monitoring.

Important: this explanation should be updated if the implementation
changes.

------------------------------------------------------------------------

## 30. Claims to Avoid Until Verified

Do not claim the project currently has:

-   production-grade Kafka streaming,
-   a fully implemented streaming architecture,
-   fully working WebSocket alerts,
-   complete production authentication,
-   a complete transaction-history API,
-   verified production deployment,
-   independently labeled fraud ground truth,
-   literal 1-bit model quantization,
-   metrics that have not actually been measured.

Describe partial functionality as partial functionality.

------------------------------------------------------------------------

## 31. Final Mental Model

Think of the system as five layers:

``` text
LAYER 1 — DATA
Dataset + transaction attributes

LAYER 2 — INTELLIGENCE
Feature engineering + anomaly detection + XGBoost

LAYER 3 — INFERENCE
ONNX + optimized runtime

LAYER 4 — APPLICATION
FastAPI + PostgreSQL + Redis + authentication

LAYER 5 — USER INTERFACE
React dashboard + scoring + history + alerts
```

The most important engineering principle is that all five layers must
agree on the same transaction representation and model feature ordering.

------------------------------------------------------------------------

## 32. Current Status

The inspected codebase contains:

-   transaction dataset,
-   feature engineering utilities,
-   Isolation Forest,
-   XGBoost,
-   evaluation code,
-   ONNX conversion/optimization scripts,
-   FastAPI backend,
-   PostgreSQL integration,
-   Redis integration,
-   JWT utilities,
-   React frontend,
-   tests,
-   Graphify project-analysis artifacts.

The next priority is to clean and synchronize the existing
implementation, then improve it incrementally.

------------------------------------------------------------------------

# End of Project Knowledge
