import React, { useState, useEffect } from 'react';

export function TodoList({ userId }) {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newTodoTitle, setNewTodoTitle] = useState('');

  useEffect(() => {
    fetchTodos();
  }, [userId]);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/todos/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch todos');
      const data = await response.json();
      setTodos(data.todos);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const createTodo = async (e) => {
    e.preventDefault();
    if (!newTodoTitle.trim()) return;

    try {
      const response = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: newTodoTitle,
          user_id: userId
        })
      });

      if (!response.ok) throw new Error('Failed to create todo');

      setNewTodoTitle('');
      fetchTodos();
    } catch (err) {
      setError(err.message);
    }
  };

  const toggleComplete = async (todoId) => {
    try {
      const response = await fetch(`/api/todos/${todoId}/complete`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId })
      });

      if (!response.ok) throw new Error('Failed to update todo');

      fetchTodos();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="todo-list">
      <h1>My Todos</h1>

      <form onSubmit={createTodo}>
        <input
          type="text"
          value={newTodoTitle}
          onChange={(e) => setNewTodoTitle(e.target.value)}
          placeholder="Add new todo..."
          data-testid="new-todo-input"
        />
        <button type="submit" data-testid="add-todo-button">
          Add
        </button>
      </form>

      <ul>
        {todos.map(todo => (
          <li key={todo.todo_id} data-testid={`todo-${todo.todo_id}`}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleComplete(todo.todo_id)}
              data-testid={`todo-checkbox-${todo.todo_id}`}
            />
            <span className={todo.completed ? 'completed' : ''}>
              {todo.title}
            </span>
          </li>
        ))}
      </ul>

      {todos.length === 0 && (
        <p data-testid="empty-message">No todos yet. Add one above!</p>
      )}
    </div>
  );
}
