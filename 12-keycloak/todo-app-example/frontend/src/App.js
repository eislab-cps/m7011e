import React, { useState, useEffect } from 'react';
import Keycloak from 'keycloak-js';
import { keycloakConfig } from './keycloak-config';
import { getTodos, createTodo, deleteTodo, toggleTodo } from './api';
import './App.css';

// Initialize Keycloak outside component to prevent multiple instances
let keycloakInstance = null;
const getKeycloak = () => {
  if (!keycloakInstance) {
    keycloakInstance = new Keycloak(keycloakConfig);
  }
  return keycloakInstance;
};

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [todos, setTodos] = useState([]);
  const [newTodoText, setNewTodoText] = useState('');
  const [error, setError] = useState(null);

  // Initialize Keycloak
  useEffect(() => {
    const keycloak = getKeycloak();

    // Check if already initialized
    if (keycloak.authenticated !== undefined) {
      setAuthenticated(keycloak.authenticated);
      setLoading(false);
      return;
    }

    keycloak.init({
      onLoad: 'login-required',
      checkLoginIframe: false
    }).then(authenticated => {
      setAuthenticated(authenticated);
      setLoading(false);

      if (authenticated) {
        // Load user profile
        keycloak.loadUserProfile().then(profile => {
          // Check if user has admin role
          const isAdmin = keycloak.hasRealmRole('admin');
          setUser({
            ...profile,
            isAdmin
          });
        });

        // Load todos
        loadTodos();
      }
    }).catch(err => {
      console.error('Keycloak initialization error:', err);
      setError('Failed to initialize authentication');
      setLoading(false);
    });

    // Setup token refresh (every 60 seconds, refresh if expires in < 70 seconds)
    const refreshInterval = setInterval(() => {
      keycloak.updateToken(70).then(refreshed => {
        if (refreshed) {
          console.log('Token refreshed');
        }
      }).catch(() => {
        console.error('Token refresh failed');
      });
    }, 60000);

    return () => clearInterval(refreshInterval);
  }, []);

  const loadTodos = async () => {
    try {
      const data = await getTodos(getKeycloak().token);
      setTodos(data);
      setError(null);
    } catch (err) {
      console.error('Error loading todos:', err);
      setError(err.message);
    }
  };

  const handleAddTodo = async (e) => {
    e.preventDefault();
    if (!newTodoText.trim()) return;

    try {
      await createTodo(getKeycloak().token, newTodoText);
      setNewTodoText('');
      await loadTodos();
      setError(null);
    } catch (err) {
      console.error('Error creating todo:', err);
      setError(err.message);
    }
  };

  const handleDeleteTodo = async (todoId) => {
    try {
      await deleteTodo(getKeycloak().token, todoId);
      await loadTodos();
      setError(null);
    } catch (err) {
      console.error('Error deleting todo:', err);
      setError(err.message);
    }
  };

  const handleToggleTodo = async (todoId) => {
    try {
      await toggleTodo(getKeycloak().token, todoId);
      await loadTodos();
      setError(null);
    } catch (err) {
      console.error('Error toggling todo:', err);
      setError(err.message);
    }
  };

  const handleLogout = () => {
    getKeycloak().logout({
      redirectUri: window.location.origin
    });
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (!authenticated) {
    return (
      <div className="app">
        <div className="error-container">
          <h2>Authentication Required</h2>
          <p>Please log in to access the todo app.</p>
          <button
            onClick={() => getKeycloak().login()}
            className="login-button"
          >
            Log In
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🔐 Secure Todo App</h1>
          <div className="user-info">
            <span className="welcome">
              Welcome, <strong>{user?.firstName || user?.username}</strong>!
              {user?.isAdmin && <span className="admin-badge">Admin</span>}
            </span>
            <button onClick={handleLogout} className="btn btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {error && (
            <div className="error-message">
              <span>⚠️ {error}</span>
              <button onClick={() => setError(null)} className="close-btn">×</button>
            </div>
          )}

          <div className="card">
            <h2>My Todos {user?.isAdmin && '(Admin View - All Users)'}</h2>

            <form onSubmit={handleAddTodo} className="todo-form">
              <input
                type="text"
                value={newTodoText}
                onChange={(e) => setNewTodoText(e.target.value)}
                placeholder="What needs to be done?"
                className="todo-input"
                autoFocus
              />
              <button type="submit" className="btn btn-primary">
                Add Todo
              </button>
            </form>

            <div className="todos-list">
              {todos.length === 0 ? (
                <p className="empty-state">No todos yet. Add one above!</p>
              ) : (
                todos.map(todo => (
                  <div key={todo.id} className="todo-item">
                    <div className="todo-content">
                      <input
                        type="checkbox"
                        checked={todo.completed || false}
                        onChange={() => handleToggleTodo(todo.id)}
                        className="todo-checkbox"
                      />
                      <span className={todo.completed ? 'todo-text completed' : 'todo-text'}>
                        {todo.text}
                      </span>
                      {user?.isAdmin && todo.username && (
                        <span className="todo-owner">by {todo.username}</span>
                      )}
                    </div>
                    <button
                      onClick={() => handleDeleteTodo(todo.id)}
                      className="btn btn-danger btn-sm"
                    >
                      Delete
                    </button>
                  </div>
                ))
              )}
            </div>

            <div className="todo-stats">
              <span>{todos.filter(t => !t.completed).length} active</span>
              <span>{todos.filter(t => t.completed).length} completed</span>
              <span>{todos.length} total</span>
            </div>
          </div>

          <div className="card info-card">
            <h3>User Information</h3>
            <dl className="user-details">
              <dt>Username:</dt>
              <dd>{user?.username}</dd>

              <dt>Email:</dt>
              <dd>{user?.email}</dd>

              <dt>Name:</dt>
              <dd>{user?.firstName} {user?.lastName}</dd>

              <dt>Roles:</dt>
              <dd>
                {user?.isAdmin ? (
                  <span className="role-badge admin">Admin</span>
                ) : (
                  <span className="role-badge user">User</span>
                )}
              </dd>
            </dl>

            <details className="token-details">
              <summary>View Access Token (for debugging)</summary>
              <pre className="token-display">{getKeycloak().token}</pre>
              <a
                href={`https://jwt.io/#debugger-io?token=${getKeycloak().token}`}
                target="_blank"
                rel="noopener noreferrer"
                className="jwt-link"
              >
                Decode at jwt.io →
              </a>
            </details>
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>
          Secured with Keycloak | Tutorial 10 - M7011E
        </p>
      </footer>
    </div>
  );
}

export default App;
