from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime, timezone

app = Flask(__name__)


# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "tododb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def create_todo(title, description, user_id):
    """Create a new todo item"""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title is required")

    if len(title) > 200:
        raise ValueError("Title too long (max 200 characters)")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO todos (title, description, user_id, completed, created_at)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING todo_id
        """,
        (title, description, user_id, False, datetime.now(timezone.utc)),
    )

    todo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return todo_id


def get_todos_by_user(user_id):
    """Get all todos for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT todo_id, title, description, completed, created_at
        FROM todos
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    todos = []
    for row in cursor.fetchall():
        todos.append(
            {
                "todo_id": row[0],
                "title": row[1],
                "description": row[2],
                "completed": row[3],
                "created_at": row[4].isoformat(),
            }
        )

    cursor.close()
    conn.close()

    return todos


def mark_todo_complete(todo_id, user_id):
    """Mark a todo as complete"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE todos
        SET completed = true
        WHERE todo_id = %s AND user_id = %s
        RETURNING todo_id
        """,
        (todo_id, user_id),
    )

    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if not result:
        raise ValueError("Todo not found or unauthorized")

    return True


@app.route("/api/todos", methods=["POST"])
def create_todo_endpoint():
    """Create todo endpoint"""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    try:
        todo_id = create_todo(
            data.get("title"), data.get("description"), data.get("user_id")
        )

        return jsonify({"todo_id": todo_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/todos/<int:user_id>", methods=["GET"])
def get_todos_endpoint(user_id):
    """Get user todos endpoint"""
    try:
        todos = get_todos_by_user(user_id)
        return jsonify({"todos": todos}), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/todos/<int:todo_id>/complete", methods=["PUT"])
def complete_todo_endpoint(todo_id):
    """Mark todo complete endpoint"""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400
    user_id = data.get("user_id")

    try:
        mark_todo_complete(todo_id, user_id)
        return jsonify({"success": True}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
