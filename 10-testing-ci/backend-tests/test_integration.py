import pytest
import psycopg2
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))

from todo_service import create_todo, get_todos_by_user, mark_todo_complete

# Use a disposable PostgreSQL instance; this fixture recreates the test DB.
import os

TEST_DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": "test_tododb",
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}


@pytest.fixture(scope="module")
def test_database():
    """Set up test database"""
    # Connect to default database to create test database
    conn = psycopg2.connect(
        host=TEST_DB_CONFIG["host"],
        port=TEST_DB_CONFIG["port"],
        database="postgres",
        user=TEST_DB_CONFIG["user"],
        password=TEST_DB_CONFIG["password"],
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Create test database
    cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB_CONFIG['database']}")
    cursor.execute(f"CREATE DATABASE {TEST_DB_CONFIG['database']}")
    cursor.close()
    conn.close()

    # Connect to test database and create schema
    conn = psycopg2.connect(**TEST_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            todo_id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            user_id INTEGER NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

    yield TEST_DB_CONFIG

    # Cleanup
    conn = psycopg2.connect(
        host=TEST_DB_CONFIG["host"],
        port=TEST_DB_CONFIG["port"],
        database="postgres",
        user=TEST_DB_CONFIG["user"],
        password=TEST_DB_CONFIG["password"],
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB_CONFIG['database']}")
    cursor.close()
    conn.close()


@pytest.fixture(autouse=True)
def clean_database(test_database, monkeypatch):
    """Direct the service to the test DB and clean it before each test."""
    monkeypatch.setattr(
        "todo_service.get_db_connection", lambda: psycopg2.connect(**test_database)
    )
    conn = psycopg2.connect(**test_database)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos")
    conn.commit()
    cursor.close()
    conn.close()


class TestTodoIntegration:
    """Integration tests with real database"""

    def test_create_and_retrieve_todo(self, test_database):
        """Test creating and retrieving a todo"""
        # Create todo
        todo_id = create_todo("Integration test todo", "Test description", 1)

        assert todo_id is not None
        assert isinstance(todo_id, int)

        # Retrieve todos
        todos = get_todos_by_user(1)

        assert len(todos) == 1
        assert todos[0]["todo_id"] == todo_id
        assert todos[0]["title"] == "Integration test todo"
        assert todos[0]["completed"] == False

    def test_multiple_users_isolation(self, test_database):
        """Test that users only see their own todos"""
        # Create todos for different users
        user1_todo = create_todo("User 1 todo", "Description", 1)
        user2_todo = create_todo("User 2 todo", "Description", 2)

        # User 1 should only see their todo
        user1_todos = get_todos_by_user(1)
        assert len(user1_todos) == 1
        assert user1_todos[0]["todo_id"] == user1_todo

        # User 2 should only see their todo
        user2_todos = get_todos_by_user(2)
        assert len(user2_todos) == 1
        assert user2_todos[0]["todo_id"] == user2_todo

    def test_mark_todo_complete_workflow(self, test_database):
        """Test complete todo workflow"""
        # Create todo
        todo_id = create_todo("Complete me", "Test", 1)

        # Verify it's not complete
        todos = get_todos_by_user(1)
        assert todos[0]["completed"] == False

        # Mark complete
        mark_todo_complete(todo_id, 1)

        # Verify it's complete
        todos = get_todos_by_user(1)
        assert todos[0]["completed"] == True

    def test_mark_complete_wrong_user_fails(self, test_database):
        """Test user cannot complete another user's todo"""
        # User 1 creates todo
        todo_id = create_todo("User 1 todo", "Description", 1)

        # User 2 tries to complete it
        with pytest.raises(ValueError, match="Todo not found"):
            mark_todo_complete(todo_id, 2)
