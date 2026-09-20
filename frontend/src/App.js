import React, { useState } from "react";
import axios from "axios";

import Dashboard from "./Dashboard";
import TransactionScore from "./components/TransactionScore";

const API_URL = "http://localhost:8000";

function App() {
  const [token, setToken] = useState(
    localStorage.getItem("finshield_token")
  );

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");

  const handleLogin = async (event) => {
    event.preventDefault();
    setLoginError("");

    try {
      const response = await axios.post(
        `${API_URL}/token`,
        {
          username,
          password
        }
      );

      const accessToken = response.data.access_token;

      localStorage.setItem(
        "finshield_token",
        accessToken
      );

      setToken(accessToken);
    } catch (error) {
      setLoginError(
        error.response?.data?.detail ||
        "Login failed"
      );
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("finshield_token");
    setToken(null);
  };

  if (!token) {
    return (
      <div className="login-page">
        <div className="login-card">
          <h1>FinShield</h1>
          <p>Fraud Detection & Monitoring</p>

          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(event) =>
                setUsername(event.target.value)
              }
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
            />

            <button type="submit">
              Sign In
            </button>
          </form>

          {loginError && (
            <p className="error">
              {loginError}
            </p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1>FinShield</h1>
          <p>Real-Time Fraud Monitoring</p>
        </div>

        <button
          className="logout-button"
          onClick={handleLogout}
        >
          Logout
        </button>
      </header>

      <main>
        <TransactionScore token={token} />

        <Dashboard token={token} />
      </main>
    </div>
  );
}

export default App;