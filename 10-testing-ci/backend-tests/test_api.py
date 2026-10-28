import pytest
from unittest.mock import patch
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))

from todo_service import app


@pytest.fixture
def client():
    """Flask test client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestTodoAPI:
    """Test Flask API endpoints"""

    @patch("todo_service.create_todo")
    def test_create_todo_endpoint_success(self, mock_create, client):
        """Test POST /api/todos success"""
        # Arrange
        mock_create.return_value = 123

        # Act
        response = client.post(
            "/api/todos",
            data=json.dumps(
                {"title": "Test todo", "description": "Test description", "user_id": 1}
            ),
            content_type="application/json",
        )

        # Assert
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["todo_id"] == 123

    @patch("todo_service.create_todo")
    def test_create_todo_endpoint_validation_error(self, mock_create, client):
        """Test POST /api/todos with validation error"""
        # Arrange
        mock_create.side_effect = ValueError("Title is required")

        # Act
        response = client.post(
            "/api/todos",
            data=json.dumps({"title": "", "description": "Test", "user_id": 1}),
            content_type="application/json",
        )

        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    @patch("todo_service.get_todos_by_user")
    def test_get_todos_endpoint(self, mock_get_todos, client):
        """Test GET /api/todos/<user_id>"""
        # Arrange
        mock_get_todos.return_value = [
            {
                "todo_id": 1,
                "title": "Test todo",
                "description": "Test",
                "completed": False,
                "created_at": "2024-01-15T10:30:00",
            }
        ]

        # Act
        response = client.get("/api/todos/1")

        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "todos" in data
        assert len(data["todos"]) == 1
        assert data["todos"][0]["title"] == "Test todo"

    @patch("todo_service.mark_todo_complete")
    def test_complete_todo_endpoint_success(self, mock_complete, client):
        """Test PUT /api/todos/<id>/complete"""
        # Arrange
        mock_complete.return_value = True

        # Act
        response = client.put(
            "/api/todos/1/complete",
            data=json.dumps({"user_id": 1}),
            content_type="application/json",
        )

        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] == True

    @patch("todo_service.mark_todo_complete")
    def test_complete_todo_endpoint_not_found(self, mock_complete, client):
        """Test PUT /api/todos/<id>/complete with non-existent todo"""
        # Arrange
        mock_complete.side_effect = ValueError("Todo not found")

        # Act
        response = client.put(
            "/api/todos/999/complete",
            data=json.dumps({"user_id": 1}),
            content_type="application/json",
        )

        # Assert
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data
