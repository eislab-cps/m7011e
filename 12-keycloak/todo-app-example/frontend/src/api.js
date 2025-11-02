// API helper functions for communicating with the backend

const API_BASE_URL = 'http://localhost:5000/api';

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

  // Handle 204 No Content responses
  if (response.status === 204) {
    return null;
  }

  return response.json();
};

// Get all todos
export const getTodos = async (token) => {
  return authFetch(`${API_BASE_URL}/todos`, token);
};

// Create a new todo
export const createTodo = async (token, text) => {
  return authFetch(`${API_BASE_URL}/todos`, token, {
    method: 'POST',
    body: JSON.stringify({ text })
  });
};

// Delete a todo
export const deleteTodo = async (token, todoId) => {
  return authFetch(`${API_BASE_URL}/todos/${todoId}`, token, {
    method: 'DELETE'
  });
};

// Toggle todo completion
export const toggleTodo = async (token, todoId) => {
  return authFetch(`${API_BASE_URL}/todos/${todoId}/toggle`, token, {
    method: 'PUT'
  });
};
