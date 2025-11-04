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

  const handleLogout = () => {
    getKeycloak().logout();
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Initializing authentication...</p>
      </div>
    );
  }

  if (!authenticated) {
    return (
      <div className="loading">
        <div className="error-container">
          <h2>Not Authenticated</h2>
          <p>Please log in to access the todo app.</p>
          <button className="login-button" onClick={() => getKeycloak().login()}>
            Login with Keycloak
          </button>
        </div>
      </div>
    );
  }

  const completedCount = todos.filter(t => t.completed).length;
  const activeCount = todos.length - completedCount;

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>My Todo App</h1>
          <div className="user-info">
            <span className="welcome">
              Welcome, {user?.firstName || user?.username}!
              {user?.isAdmin && <span className="admin-badge">Admin</span>}
            </span>
            <button className="btn btn-secondary btn-sm" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {error && (
            <div className="error-message">
              <span>{error}</span>
              <button className="close-btn" onClick={() => setError(null)}>×</button>
            </div>
          )}

          <div className="card">
            <h2>Add New Todo</h2>
            <form className="todo-form" onSubmit={handleAddTodo}>
              <input
                type="text"
                className="todo-input"
                placeholder="What needs to be done?"
                value={newTodoText}
                onChange={(e) => setNewTodoText(e.target.value)}
              />
              <button type="submit" className="btn btn-primary">
                Add Todo
              </button>
            </form>
          </div>

          <div className="card">
            <h2>My Todos</h2>
            {todos.length === 0 ? (
              <div className="empty-state">
                No todos yet. Add one above to get started!
              </div>
            ) : (
              <>
                <div className="todos-list">
                  {todos.map(todo => (
                    <div key={todo.id} className="todo-item">
                      <div className="todo-content">
                        <input
                          type="checkbox"
                          className="todo-checkbox"
                          checked={todo.completed}
                          onChange={() => handleToggleTodo(todo.id)}
                        />
                        <span className={`todo-text ${todo.completed ? 'completed' : ''}`}>
                          {todo.text}
                        </span>
                        {todo.username && todo.username !== user?.username && (
                          <span className="todo-owner">by {todo.username}</span>
                        )}
                      </div>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleDeleteTodo(todo.id)}
                      >
                        Delete
                      </button>
                    </div>
                  ))}
                </div>
                <div className="todo-stats">
                  <span>Total: {todos.length}</span>
                  <span>Active: {activeCount}</span>
                  <span>Completed: {completedCount}</span>
                </div>
              </>
            )}
          </div>

          <div className="card info-card">
            <h3>User Information</h3>
            <dl className="user-details">
              <dt>Name:</dt>
              <dd>{user?.firstName} {user?.lastName}</dd>
              <dt>Username:</dt>
              <dd>{user?.username}</dd>
              <dt>Email:</dt>
              <dd>{user?.email || 'N/A'}</dd>
              <dt>Role:</dt>
              <dd>
                <span className={`role-badge ${user?.isAdmin ? 'admin' : 'user'}`}>
                  {user?.isAdmin ? 'Administrator' : 'User'}
                </span>
              </dd>
            </dl>

            <details className="token-details">
              <summary>View Access Token</summary>
              <div className="token-display">
                {getKeycloak().token}
              </div>
              <p>
                <a
                  href={`https://jwt.io/#debugger-io?token=${getKeycloak().token}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="jwt-link"
                >
                  Decode on jwt.io →
                </a>
              </p>
            </details>
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>Keycloak Todo App - Part 3: WITH RBAC</p>
      </footer>
    </div>
  );
}

export default App;
