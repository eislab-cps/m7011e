import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import { TodoList } from './src/TodoList';

// Mock fetch globally
global.fetch = jest.fn();

describe('TodoList Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.resetAllMocks();
  });

  describe('Loading and Error States', () => {
    test('shows loading state initially', () => {
      // Arrange
      fetch.mockImplementation(() => new Promise(() => {})); // Never resolves

      // Act
      render(<TodoList userId={1} />);

      // Assert
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });

    test('shows error when fetch fails', async () => {
      // Arrange
      fetch.mockRejectedValueOnce(new Error('Network error'));

      // Act
      render(<TodoList userId={1} />);

      // Assert
      await waitFor(() => {
        expect(screen.getByText(/Error:/)).toBeInTheDocument();
      });
    });
  });

  describe('Fetching Todos', () => {
    test('fetches and displays todos on mount', async () => {
      // Arrange
      const mockTodos = {
        todos: [
          { todo_id: 1, title: 'Buy milk', completed: false },
          { todo_id: 2, title: 'Walk dog', completed: true }
        ]
      };

      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockTodos
      });

      // Act
      render(<TodoList userId={1} />);

      // Assert
      await waitFor(() => {
        expect(screen.getByText('Buy milk')).toBeInTheDocument();
        expect(screen.getByText('Walk dog')).toBeInTheDocument();
      });
    });

    test('shows empty message when no todos', async () => {
      // Arrange
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ todos: [] })
      });

      // Act
      render(<TodoList userId={1} />);

      // Assert
      await waitFor(() => {
        expect(screen.getByTestId('empty-message')).toBeInTheDocument();
      });
    });

    test('calls API with correct user ID', async () => {
      // Arrange
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ todos: [] })
      });

      // Act
      render(<TodoList userId={42} />);

      // Assert
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('/api/todos/42');
      });
    });
  });

  describe('Creating Todos', () => {
    test('creates new todo when form submitted', async () => {
      // Arrange
      fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ todos: [] })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ todo_id: 1 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            todos: [{ todo_id: 1, title: 'New todo', completed: false }]
          })
        });

      render(<TodoList userId={1} />);

      await waitFor(() => screen.getByTestId('new-todo-input'));

      // Act
      const input = screen.getByTestId('new-todo-input');
      const button = screen.getByTestId('add-todo-button');

      await userEvent.type(input, 'New todo');
      await userEvent.click(button);

      // Assert
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('/api/todos', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            title: 'New todo',
            user_id: 1
          })
        });
      });

      // Input should be cleared
      expect(input.value).toBe('');
    });

    test('does not create todo with empty title', async () => {
      // Arrange
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ todos: [] })
      });

      render(<TodoList userId={1} />);

      await waitFor(() => screen.getByTestId('add-todo-button'));

      // Act
      const button = screen.getByTestId('add-todo-button');
      await userEvent.click(button);

      // Assert
      // Only the initial fetch should have been called
      expect(fetch).toHaveBeenCalledTimes(1);
    });
  });

  describe('Completing Todos', () => {
    test('marks todo as complete when checkbox clicked', async () => {
      // Arrange
      const mockTodos = {
        todos: [{ todo_id: 1, title: 'Buy milk', completed: false }]
      };

      fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockTodos
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ success: true })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            todos: [{ todo_id: 1, title: 'Buy milk', completed: true }]
          })
        });

      render(<TodoList userId={1} />);

      await waitFor(() => screen.getByTestId('todo-checkbox-1'));

      // Act
      const checkbox = screen.getByTestId('todo-checkbox-1');
      await userEvent.click(checkbox);

      // Assert
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('/api/todos/1/complete', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: 1 })
        });
      });
    });
  });

  describe('Accessibility', () => {
    test('has accessible form elements', async () => {
      // Arrange
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ todos: [] })
      });

      // Act
      render(<TodoList userId={1} />);

      // Assert
      await waitFor(() => {
        const input = screen.getByPlaceholderText('Add new todo...');
        const button = screen.getByRole('button', { name: /add/i });

        expect(input).toBeInTheDocument();
        expect(button).toBeInTheDocument();
      });
    });

    test('checkboxes are keyboard accessible', async () => {
      // Arrange
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          todos: [{ todo_id: 1, title: 'Test', completed: false }]
        })
      });

      render(<TodoList userId={1} />);

      // Assert
      await waitFor(() => {
        const checkbox = screen.getByTestId('todo-checkbox-1');
        expect(checkbox).toHaveAttribute('type', 'checkbox');
      });
    });
  });
});
