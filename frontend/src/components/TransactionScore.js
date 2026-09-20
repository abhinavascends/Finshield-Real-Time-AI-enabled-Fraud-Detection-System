import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

const initialData = {
  TransactionAmount: 350.25,
  CustomerAge: 27,
  TransactionDuration: 4.2,
  LoginAttempts: 2,
  AccountBalance: 8000,

  is_large_transaction: 0,
  log_transaction_amount: 5.86,
  transaction_hour: 16,
  transaction_day_of_week: 3,
  odd_hour_transaction: 0,

  user_transaction_count: 12,
  user_avg_transaction_amount: 300,
  deviation_from_user_avg: 50.25,

  TransactionType: "Credit",
  Location: "Los Angeles",
  Channel: "Web",
  CustomerOccupation: "Designer",
  user_primary_location: "Los Angeles",

  is_unusual_location: 0
};

const numericFields = new Set([
  "TransactionAmount",
  "CustomerAge",
  "TransactionDuration",
  "LoginAttempts",
  "AccountBalance",
  "is_large_transaction",
  "log_transaction_amount",
  "transaction_hour",
  "transaction_day_of_week",
  "odd_hour_transaction",
  "user_transaction_count",
  "user_avg_transaction_amount",
  "deviation_from_user_avg",
  "is_unusual_location"
]);

export default function TransactionScore({ token }) {
  const [form, setForm] = useState(initialData);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setResult(null);
    setError("");

    const payload = Object.fromEntries(
      Object.entries(form).map(
        ([key, value]) => [
          key,
          numericFields.has(key)
            ? Number(value)
            : value
        ]
      )
    );

    try {
      const response = await axios.post(
        `${API_URL}/transactions/score`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setResult(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to score transaction"
      );
    }
  };

  return (
    <section className="score-panel">
      <div className="panel-header">
        <div>
          <h2>Transaction Risk Scoring</h2>
          <p>
            Submit a transaction to the fraud detection model.
          </p>
        </div>
      </div>

      <form
        className="transaction-form"
        onSubmit={handleSubmit}
      >
        {Object.entries(form).map(
          ([key, value]) => (
            <div
              className="form-field"
              key={key}
            >
              <label htmlFor={key}>
                {key}
              </label>

              <input
                id={key}
                name={key}
                value={value}
                onChange={handleChange}
                type={
                  numericFields.has(key)
                    ? "number"
                    : "text"
                }
                step={
                  [
                    "TransactionAmount",
                    "TransactionDuration",
                    "AccountBalance",
                    "log_transaction_amount",
                    "user_transaction_count",
                    "user_avg_transaction_amount",
                    "deviation_from_user_avg"
                  ].includes(key)
                    ? "any"
                    : "1"
                }
              />
            </div>
          )
        )}

        <button type="submit">
          Score Transaction
        </button>
      </form>

      {result && (
        <div className="score-result">
          <h3>Model Result</h3>

          <div className="result-grid">
            <div>
              <span>Fraud Probability</span>
              <strong>
                {Number(
                  result.fraud_probability
                ).toFixed(4)}
              </strong>
            </div>

            <div>
              <span>Risk Status</span>
              <strong
                className={
                  result.is_fraud
                    ? "risk-fraud"
                    : "risk-safe"
                }
              >
                {result.is_fraud
                  ? "HIGH RISK"
                  : "LOW RISK"}
              </strong>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="error">
          {error}
        </div>
      )}
    </section>
  );
}