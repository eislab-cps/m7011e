import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))

from todo_service import create_todo, get_todos_by_user, mark_todo_complete


class TestCreateTodo:
    """Unit tests for create_todo function"""

    @patch("todo_service.get_db_connection")
    def test_create_todo_success(self, mock_get_db):
        """Test creating a todo successfully"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [123]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn

        # Act
        todo_id = create_todo("Buy milk", "From the store", 1)

        # Assert
        assert todo_id == 123
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("todo_service.get_db_connection")
    def test_create_todo_empty_title_fails(self, mock_get_db):
        """Test that empty title raises ValueError"""
        # Act & Assert
        with pytest.raises(ValueError, match="Title is required"):
            create_todo("", "Description", 1)

        # Database should not be called
        mock_get_db.assert_not_called()

    @patch("todo_service.get_db_connection")
    def test_create_todo_long_title_fails(self, mock_get_db):
        """Test that title > 200 chars raises ValueError"""
        long_title = "a" * 201

        # Act & Assert
        with pytest.raises(ValueError, match="Title too long"):
            create_todo(long_title, "Description", 1)

        # Database should not be called
        mock_get_db.assert_not_called()


class TestGetTodosByUser:
    """Unit tests for get_todos_by_user function"""

    @patch("todo_service.get_db_connection")
    def test_get_todos_returns_list(self, mock_get_db):
        """Test getting todos returns correct format"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, "Buy milk", "From store", False, datetime(2024, 1, 15, 10, 30)),
            (2, "Walk dog", "In park", True, datetime(2024, 1, 15, 11, 0)),
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn

        # Act
        todos = get_todos_by_user(1)

        # Assert
        assert len(todos) == 2
        assert todos[0]["todo_id"] == 1
        assert todos[0]["title"] == "Buy milk"
        assert todos[0]["completed"] == False
        assert todos[1]["todo_id"] == 2
        assert todos[1]["completed"] == True

    @patch("todo_service.get_db_connection")
    def test_get_todos_empty_list(self, mock_get_db):
        """Test getting todos for user with no todos"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn

        # Act
        todos = get_todos_by_user(999)

        # Assert
        assert todos == []


class TestMarkTodoComplete:
    """Unit tests for mark_todo_complete function"""

    @patch("todo_service.get_db_connection")
    def test_mark_complete_success(self, mock_get_db):
        """Test marking todo as complete"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [1]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn

        # Act
        result = mark_todo_complete(1, 1)

        # Assert
        assert result == True
        mock_conn.commit.assert_called_once()

    @patch("todo_service.get_db_connection")
    def test_mark_complete_not_found(self, mock_get_db):
        """Test marking non-existent todo fails"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_conn

        # Act & Assert
        with pytest.raises(ValueError, match="Todo not found"):
            mark_todo_complete(999, 1)


# Pytest fixtures for reusable test setup
@pytest.fixture
def mock_db_connection():
    """Fixture to provide a mocked database connection"""
    with patch("todo_service.get_db_connection") as mock:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock.return_value = mock_conn
        yield {"connection": mock_conn, "cursor": mock_cursor, "get_db": mock}
