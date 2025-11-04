// API helper functions for communicating with the backend

const API_BASE_URL = 'http://localhost:5001/api';

// Helper function to make authenticated requests
const authFetch = async (url, token, options = {}) => {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Request failed' }));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
};

// Call the protected endpoint to test JWT authentication
export const callProtectedAPI = async (token) => {
  return authFetch(`${API_BASE_URL}/protected`, token);
};
