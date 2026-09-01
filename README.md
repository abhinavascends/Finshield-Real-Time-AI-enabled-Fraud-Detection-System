# FinShield
## AI-Enabled Real-Time Transaction Fraud Detection System

## Overview

FinShield is a transaction fraud detection system that combines machine
learning with a backend API and application infrastructure to evaluate
financial transactions for anomalous and potentially fraudulent activity.

The project is being developed as a modular pipeline that progresses from
transaction data and feature engineering to anomaly detection, supervised
classification, model inference, and application-level transaction
processing.

## Problem

Financial transaction data can contain patterns that differ from normal
account activity. Suspicious behaviour may be associated with transaction
amounts, account activity, transaction timing, transaction channels,
locations, and other transaction-level attributes.

The objective of FinShield is to develop a machine-learning based pipeline
that can transform transaction data into model-ready representations and
use those representations to identify transactions requiring further
fraud-risk evaluation.

## Technology Stack

### Machine Learning
- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost

### Backend
- FastAPI
- Python

### Data & Infrastructure
- PostgreSQL
- Redis

### Frontend
- React
- JavaScript

### Development & Testing
- Git
- GitHub
- Pytest

## Project Structure

```text
FinShield/
│
├── app/                 # Backend application and API logic
├── model/               # Machine-learning training and inference code
├── Database/            # Database schema and persistence definitions
├── frontend/            # React application
├── tests/               # Automated tests
│
├── bank_transactions_featured.csv
├── Feature_Generation.py
├── IsolationForest.ipynb
├── isolationforest.py
├── requirements.txt
└── README.md
```

## Development Direction

The system is being developed incrementally through the following stages:

```text
Transaction Dataset
        ↓
Feature Engineering
        ↓
Feature Preprocessing
        ↓
Anomaly Detection
        ↓
Supervised Fraud Classification
        ↓
Production Inference
        ↓
Transaction API
        ↓
Persistence & Alert Infrastructure
        ↓
Monitoring Dashboard
```

The initial implementation focuses on establishing a clean project
foundation and preparing the transaction data and feature pipeline before
moving into model development and application integration.
