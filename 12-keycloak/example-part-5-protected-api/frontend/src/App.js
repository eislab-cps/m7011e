import React, { useState, useEffect } from 'react';
import keycloak from './keycloak';
import { callProtectedAPI } from './api';
import './App.css';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  // NEW in Part 5: State for API testing
  const [apiResponse, setApiResponse] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Initialize Keycloak
    keycloak.init({
      onLoad: 'login-required',
      checkLoginIframe: false
    }).then(authenticated => {
      setAuthenticated(authenticated);

      if (authenticated) {
        keycloak.loadUserProfile().then(profile => {
          setUser(profile);
        });
      }
    });
  }, []);

  // NEW in Part 5: Function to call the protected API
  const handleCallAPI = async () => {
    try {
      setError(null);

      // Refresh token if needed (within 30 seconds of expiry)
      await keycloak.updateToken(30);

      // Call the protected API with the current token
      const data = await callProtectedAPI(keycloak.token);

      setApiResponse(data);
      console.log('API response:', data);
    } catch (err) {
      console.error('API call failed:', err);
      setError(err.message);
    }
  };

  const logout = () => {
    keycloak.logout();
  };

  if (!authenticated) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Part 5: Protected API Call</h1>
        <h2>Welcome, {user?.firstName} {user?.lastName}!</h2>
        <p>Email: {user?.email}</p>
        <p>Username: {user?.username}</p>

        {/* NEW in Part 5: Button to test API */}
        <div style={{ marginTop: '20px' }}>
          <button onClick={handleCallAPI}>
            Call Protected API
          </button>
        </div>

        {/* NEW in Part 5: Display API response */}
        {apiResponse && (
          <div style={{
            marginTop: '20px',
            padding: '15px',
            background: '#e8f5e9',
            color: '#1b5e20',
            borderRadius: '5px',
            maxWidth: '600px'
          }}>
            <h3>✅ API Response:</h3>
            <pre style={{
              background: '#fff',
              color: '#000',
              padding: '10px',
              fontSize: '14px'
            }}>
              {JSON.stringify(apiResponse, null, 2)}
            </pre>
          </div>
        )}

        {/* NEW in Part 5: Display errors */}
        {error && (
          <div style={{
            marginTop: '20px',
            padding: '15px',
            background: '#ffebee',
            color: '#c62828',
            borderRadius: '5px',
            maxWidth: '600px'
          }}>
            <strong>❌ Error:</strong> {error}
          </div>
        )}

        <h3>Your Access Token</h3>
        <pre style={{ fontSize: '10px', overflow: 'auto', maxWidth: '800px' }}>
          {keycloak.token}
        </pre>

        <button onClick={logout}>Logout</button>
      </header>
    </div>
  );
}

export default App;
