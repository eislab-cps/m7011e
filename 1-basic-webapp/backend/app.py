"""
Simple Todo List REST API

This Flask application demonstrates basic REST API principles:
- GET /api/todos - Retrieve all todos
- POST /api/todos - Create a new todo
- DELETE /api/todos/<id> - Delete a todo

Data is stored in-memory (resets when server restarts).
In a real application, you would use a database.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)

# Enable CORS to allow requests from frontend (different port/origin)
# Allow all origins for development - in production, specify exact origins
CORS(app, resources={r"/api/*": {"origins": "*"}})

# In-memory storage for todos (will be reset when server restarts)
# In production, you would use a database like PostgreSQL, MongoDB, etc.
todos = []

# Counter for generating unique IDs
next_id = 1


@app.route('/api/todos', methods=['GET'])
def get_todos():
    """
    GET /api/todos

    Retrieve all todos.

    Returns:
        JSON array of todo objects
        Example: [{"id": 1, "text": "Learn Flask"}]
    """
    return jsonify(todos), 200


@app.route('/api/todos', methods=['POST'])
def create_todo():
    """
    POST /api/todos

    Create a new todo.

    Request body (JSON):
        {"text": "Todo text here"}

    Returns:
        JSON object of created todo with assigned ID
        Status: 201 Created
    """
    global next_id

    # Get JSON data from request body
    data = request.json

    # Validate that 'text' field exists
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400

    # Validate that text is not empty
    if not data['text'].strip():
        return jsonify({'error': 'Text cannot be empty'}), 400

    # Create new todo with unique ID
    new_todo = {
        'id': next_id,
        'text': data['text'].strip()
    }

    # Add to our in-memory list
    todos.append(new_todo)

    # Increment ID counter for next todo
    next_id += 1

    # Return created todo with 201 status (Created)
    return jsonify(new_todo), 201


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """
    DELETE /api/todos/<id>

    Delete a todo by ID.

    Parameters:
        todo_id (int): ID of todo to delete

    Returns:
        Empty response with 204 status (No Content) if successful
        404 status if todo not found
    """
    global todos

    # Find the todo with matching ID
    todo = next((t for t in todos if t['id'] == todo_id), None)

    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404

    # Remove todo from list (filter out the deleted todo)
    todos = [t for t in todos if t['id'] != todo_id]

    # Return empty response with 204 status (No Content)
    return '', 204


@app.route('/')
def home():
    """
    Root endpoint - provides API information
    """
    return jsonify({
        'message': 'Todo List REST API',
        'endpoints': {
            'GET /api/todos': 'Get all todos',
            'POST /api/todos': 'Create a new todo',
            'DELETE /api/todos/<id>': 'Delete a todo'
        }
    })


# Run the application
if __name__ == '__main__':
    # debug=True enables auto-reload and detailed error messages
    # Don't use debug=True in production!
    print("Starting Flask server...")
    print("API will be available at: http://127.0.0.1:5000")
    print("API endpoints:")
    print("  GET    http://127.0.0.1:5000/api/todos")
    print("  POST   http://127.0.0.1:5000/api/todos")
    print("  DELETE http://127.0.0.1:5000/api/todos/<id>")
    print("\nPress CTRL+C to stop the server")

    app.run(debug=True, host='127.0.0.1', port=5000)
