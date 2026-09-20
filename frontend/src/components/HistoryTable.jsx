import React from "react";

const HistoryTable = ({ transactions = [] }) => {
  if (transactions.length === 0) {
    return (
      <div className="history-table">
        <h3>Transaction History</h3>
        <p>No transactions found.</p>
      </div>
    );
  }

  return (
    <div className="history-table">
      <h3>Transaction History</h3>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Amount</th>
              <th>Location</th>
              <th>Fraud Probability</th>
              <th>Status</th>
              <th>Time</th>
            </tr>
          </thead>

          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.id}>
                <td>#{transaction.id}</td>

                <td>
                  ${Number(
                    transaction.amount || 0
                  ).toFixed(2)}
                </td>

                <td>
                  {transaction.location || "-"}
                </td>

                <td>
                  {transaction.fraud_probability !==
                  null &&
                  transaction.fraud_probability !==
                  undefined
                    ? Number(
                        transaction.fraud_probability
                      ).toFixed(4)
                    : "-"}
                </td>

                <td>
                  {transaction.is_fraud
                    ? "Fraud"
                    : "Safe"}
                </td>

                <td>
                  {transaction.event_time
                    ? new Date(
                        transaction.event_time
                      ).toLocaleString()
                    : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HistoryTable;