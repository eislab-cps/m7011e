// Example React component with Keycloak authentication
// Install: npm install keycloak-js

import React, { useState, useEffect } from 'react';
import Keycloak from 'keycloak-js';

// Initialize Keycloak
const keycloak = new Keycloak({
  url: 'https://keycloak.ltu-m7011e-YOUR-NAME.se',
  realm: 'm7011e',
  clientId: 'demo-app'
});

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initialize Keycloak
    keycloak.init({
      onLoad: 'login-required',
      checkLoginIframe: false
    }).then(authenticated => {
      setAuthenticated(authenticated);
      setLoading(false);

      if (authenticated) {
        // Load user profile
        keycloak.loadUserProfile().then(profile => {
          setUser(profile);
        });
      }
    }).catch(error => {
      console.error('Keycloak initialization error:', error);
      setLoading(false);
    });

    // Token refresh
    const refreshInterval = setInterval(() => {
      keycloak.updateToken(70).then(refreshed => {
        if (refreshed) {
          console.log('Token refreshed');
        }
      }).catch(() => {
        console.error('Token refresh failed');
      });
    }, 60000); // Check every 60 seconds

    return () => clearInterval(refreshInterval);
  }, []);

  const logout = () => {
    keycloak.logout({
      redirectUri: window.location.origin
    });
  };

  const hasRole = (role) => {
    return keycloak.hasRealmRole(role);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  if (!authenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Not authenticated</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-6">
          Welcome, {user?.firstName || user?.username}!
        </h1>

        <div className="mb-8 space-y-2">
          <p><strong>Username:</strong> {user?.username}</p>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>First Name:</strong> {user?.firstName}</p>
          <p><strong>Last Name:</strong> {user?.lastName}</p>
        </div>

        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Your Roles:</h2>
          <div className="space-y-2">
            {hasRole('admin') && (
              <span className="inline-block bg-red-500 text-white px-4 py-2 rounded mr-2">
                Admin
              </span>
            )}
            {hasRole('user') && (
              <span className="inline-block bg-blue-500 text-white px-4 py-2 rounded mr-2">
                User
              </span>
            )}
            {hasRole('viewer') && (
              <span className="inline-block bg-green-500 text-white px-4 py-2 rounded mr-2">
                Viewer
              </span>
            )}
          </div>
        </div>

        {hasRole('admin') && (
          <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded">
            <h2 className="text-xl font-semibold mb-2">Admin Features</h2>
            <p>You have administrator access!</p>
          </div>
        )}

        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Access Token:</h2>
          <div className="bg-gray-50 p-4 rounded overflow-x-auto">
            <pre className="text-xs">{keycloak.token}</pre>
          </div>
        </div>

        <div className="space-x-4">
          <button
            onClick={() => window.location.href = keycloak.createAccountUrl()}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded"
          >
            Manage Account
          </button>

          <button
            onClick={logout}
            className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded"
          >
            Logout
          </button>
        </div>
      </div>

      <ProtectedApiExample token={keycloak.token} />
    </div>
  );
}

// Example component showing how to make authenticated API calls
function ProtectedApiExample({ token }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchProtectedData = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('https://api.example.com/protected', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      setData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-8 bg-white rounded-lg shadow-lg p-8">
      <h2 className="text-2xl font-bold mb-4">Protected API Example</h2>

      <button
        onClick={fetchProtectedData}
        disabled={loading}
        className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded disabled:bg-gray-400"
      >
        {loading ? 'Loading...' : 'Fetch Protected Data'}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded text-red-700">
          Error: {error}
        </div>
      )}

      {data && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded">
          <pre className="text-sm">{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
