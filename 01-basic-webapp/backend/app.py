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
from flasgger import Swagger

# Initialize Flask application
app = Flask(__name__)

# Enable CORS to allow requests from frontend (different port/origin)
# Configure CORS to allow requests from any origin for development
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure Swagger UI for API documentation
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api-docs"
}

swagger_template = {
    "info": {
        "title": "Todo List REST API",
        "description": "A simple REST API for managing todo items. This demonstrates basic CRUD operations using REST principles.",
        "version": "1.0.0"
    },
    "schemes": ["http"],
    "tags": [
        {
            "name": "todos",
            "description": "Todo item operations"
        }
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# In-memory storage for todos (will be reset when server restarts)
# In production, you would use a database like PostgreSQL, MongoDB, etc.
todos = []

# Counter for generating unique IDs
next_id = 1


@app.route('/api/todos', methods=['GET'])
def get_todos():
    """
    Get all todos
    Retrieve a list of all todo items
    ---
    tags:
      - todos
    responses:
      200:
        description: A list of todos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The todo ID
                example: 1
              text:
                type: string
                description: The todo text
                example: "Learn Flask"
    """
    return jsonify(todos), 200


@app.route('/api/todos', methods=['POST'])
def create_todo():
    """
    Create a new todo
    Add a new todo item to the list
    ---
    tags:
      - todos
    parameters:
      - in: body
        name: body
        required: true
        description: Todo item to create
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              description: The todo text
              example: "Learn Flask"
    responses:
      201:
        description: Todo created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The assigned todo ID
              example: 1
            text:
              type: string
              description: The todo text
              example: "Learn Flask"
      400:
        description: Invalid request (missing or empty text)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing text field"
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
    Delete a todo
    Remove a todo item by its ID
    ---
    tags:
      - todos
    parameters:
      - in: path
        name: todo_id
        type: integer
        required: true
        description: The ID of the todo to delete
        example: 1
    responses:
      204:
        description: Todo deleted successfully (no content returned)
      404:
        description: Todo not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Todo not found"
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
    print("API will be available at: http://localhost:8000")
    print("\nAPI endpoints:")
    print("  GET    http://localhost:8000/api/todos")
    print("  POST   http://localhost:8000/api/todos")
    print("  DELETE http://localhost:8000/api/todos/<id>")
    print("\nSwagger API Documentation:")
    print("  http://localhost:8000/api-docs")
    print("  (Interactive API testing and documentation)")
    print("\nPress CTRL+C to stop the server")
    print("\nNote: Using port 8000 to avoid conflicts with system services")

    app.run(debug=True, host='0.0.0.0', port=8000)
