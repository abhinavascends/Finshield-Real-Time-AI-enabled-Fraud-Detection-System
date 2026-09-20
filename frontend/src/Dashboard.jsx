import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

const Dashboard = ({ token }) => {
  const [transactions, setTransactions] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchDashboardData = async () => {
    try {
      setError("");

      const headers = {
        Authorization: `Bearer ${token}`
      };

      const [transactionResponse, alertResponse] =
        await Promise.all([
          axios.get(
            `${API_URL}/transactions/history`,
            { headers }
          ),
          axios.get(
            `${API_URL}/alerts`,
            { headers }
          )
        ]);

      setTransactions(
        transactionResponse.data
      );

      setAlerts(
        alertResponse.data
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to load dashboard data"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();

    const interval = setInterval(
      fetchDashboardData,
      10000
    );

    return () => clearInterval(interval);
  }, [token]);

  const fraudCount = transactions.filter(
    (transaction) => transaction.is_fraud
  ).length;

  const totalTransactions =
    transactions.length;

  const fraudRate =
    totalTransactions > 0
      ? ((fraudCount / totalTransactions) * 100).toFixed(1)
      : "0.0";

  return (
    <section className="dashboard">
      <div className="dashboard-heading">
        <div>
          <h2>Monitoring Dashboard</h2>
          <p>
            Live transaction activity and fraud alerts
          </p>
        </div>

        <button
          className="refresh-button"
          onClick={fetchDashboardData}
        >
          Refresh
        </button>
      </div>

      {error && (
        <div className="error dashboard-error">
          {error}
        </div>
      )}

      <div className="metrics">
        <div className="metric-card">
          <span>Total Transactions</span>
          <strong>{totalTransactions}</strong>
        </div>

        <div className="metric-card">
          <span>Fraudulent Transactions</span>
          <strong>{fraudCount}</strong>
        </div>

        <div className="metric-card">
          <span>Fraud Rate</span>
          <strong>{fraudRate}%</strong>
        </div>

        <div className="metric-card">
          <span>Active Alerts</span>
          <strong>{alerts.length}</strong>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="panel">
          <div className="panel-header">
            <h3>Recent Transactions</h3>
          </div>

          {loading ? (
            <p>Loading transactions...</p>
          ) : transactions.length === 0 ? (
            <p>No transactions found.</p>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Amount</th>
                    <th>Location</th>
                    <th>Risk Score</th>
                    <th>Status</th>
                    <th>Time</th>
                  </tr>
                </thead>

                <tbody>
                  {transactions.map((transaction) => (
                    <tr key={transaction.id}>
                      <td>
                        #{transaction.id}
                      </td>

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
                        <span
                          className={
                            transaction.is_fraud
                              ? "status fraud"
                              : "status safe"
                          }
                        >
                          {transaction.is_fraud
                            ? "Fraud"
                            : "Safe"}
                        </span>
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
          )}
        </div>

        <div className="panel alerts-panel">
          <div className="panel-header">
            <h3>Recent Alerts</h3>
          </div>

          {alerts.length === 0 ? (
            <p>No active alerts.</p>
          ) : (
            <div className="alerts-list">
              {alerts.map((alert) => (
                <div
                  className="alert-item"
                  key={alert.id}
                >
                  <div>
                    <strong>
                      {alert.type}
                    </strong>

                    <p>
                      Transaction #
                      {alert.transaction_id}
                    </p>
                  </div>

                  <span>
                    {alert.time
                      ? new Date(
                          alert.time
                        ).toLocaleString()
                      : "-"}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default Dashboard;