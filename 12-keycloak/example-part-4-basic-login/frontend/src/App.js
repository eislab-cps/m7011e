import React, { useState, useEffect } from 'react';
import keycloak from './keycloak';
import './App.css';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Initialize Keycloak
    keycloak.init({
      onLoad: 'login-required',  // Redirect to login if not authenticated
      checkLoginIframe: false
    }).then(authenticated => {
      setAuthenticated(authenticated);

      if (authenticated) {
        // Load user profile
        keycloak.loadUserProfile().then(profile => {
          setUser(profile);
        });
      }
    });
  }, []);

  const logout = () => {
    keycloak.logout();
  };

  if (!authenticated) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Part 4: Basic Keycloak Authentication</h1>
        <h2>Welcome, {user?.firstName} {user?.lastName}!</h2>
        <p>Email: {user?.email}</p>
        <p>Username: {user?.username}</p>

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
