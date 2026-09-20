import React from "react";

const ScoreResult = ({ scoreResult }) => {
  if (!scoreResult) {
    return null;
  }

  return (
    <div className="score-result">
      <h2>Transaction Risk Result</h2>

      <p>
        Fraud Probability:{" "}
        {Number(
          scoreResult.fraud_probability
        ).toFixed(4)}
      </p>

      <p>
        Status:{" "}
        {scoreResult.is_fraud
          ? "High Risk"
          : "Low Risk"}
      </p>
    </div>
  );
};

export default ScoreResult;