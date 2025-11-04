import React, { useState, useEffect } from 'react';
import keycloak from './keycloak';
import { callProtectedAPI } from './api';  // ← NEW IMPORT

function App() {
  // Existing state
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  // NEW: State for API testing
  const [apiResponse, setApiResponse] = useState(null);
  const [error, setError] = useState(null);

  // Existing useEffect (no changes)
  useEffect(() => {
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

  // NEW: Function to call the protected API
  const handleCallAPI = async () => {
    try {
      setError(null);
      await keycloak.updateToken(30);
      const data = await callProtectedAPI(keycloak.token);
      setApiResponse(data);
      console.log('API response:', data);
    } catch (err) {
      console.error('API call failed:', err);
      setError(err.message);
    }
  };

  if (!authenticated) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Welcome, {user?.firstName} {user?.lastName}!</h1>
      <p>Email: {user?.email}</p>

      {/* NEW: Button to test API */}
      <button onClick={handleCallAPI}>
        Call Protected API
      </button>

      {/* NEW: Display API response */}
      {apiResponse && (
        <div style={{ marginTop: '20px', padding: '10px', background: '#e8f5e9' }}>
          <h3>API Response:</h3>
          <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
        </div>
      )}

      {/* NEW: Display errors */}
      {error && (
        <div style={{ marginTop: '20px', padding: '10px', background: '#ffebee', color: 'red' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Existing logout button */}
      <button onClick={() => keycloak.logout()}>Logout</button>
    </div>
  );
}

export default App;
