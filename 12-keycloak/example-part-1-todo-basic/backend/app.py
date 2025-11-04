#!/usr/bin/env python3
"""
Part 4 Example: Todo API WITHOUT Public Key Verification
This backend accepts JWT tokens but does NOT verify the signature.
This is simpler but INSECURE - use only for learning!

For production, see example-part-5 which verifies signatures properly.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from functools import wraps
from datetime import datetime

app = Flask(__name__)

# Configure CORS to allow requests from React frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# In-memory storage for todos
# In production, use a proper database (PostgreSQL, etc.)
todos = []
todo_id_counter = 1


def require_auth(f):
    """
    Decorator to require JWT token (WITHOUT signature verification)

    ⚠️ WARNING: This does NOT verify the token signature!
    This is for learning purposes only. Anyone can forge tokens.
    See example-part-5 for proper JWT verification.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401

        # Extract token (format: "Bearer <token>")
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Invalid authorization header'}), 401

        token = parts[1]

        try:
            # ⚠️ INSECURE: Decode WITHOUT verifying signature
            # This just extracts the claims without checking if token is valid!
            decoded_token = jwt.decode(
                token,
                options={
                    'verify_signature': False,  # ← INSECURE! No verification!
                    'verify_exp': False,         # Don't even check expiration
                    'verify_nbf': False,
                    'verify_iss': False,
                    'verify_aud': False
                }
            )

            # Add user information to request context
            request.user = decoded_token

            return f(*args, **kwargs)

        except Exception as e:
            print(f"Token decode error: {e}")
            return jsonify({'error': f'Invalid token: {str(e)}'}), 401

    return decorated_function


def get_user_id():
    """Extract user ID from token"""
    return request.user.get('sub')


def get_username():
    """Extract username from token"""
    return request.user.get('preferred_username', 'unknown')


def is_admin():
    """Check if the authenticated user has admin role"""
    realm_roles = request.user.get('realm_access', {}).get('roles', [])
    return 'admin' in realm_roles


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'message': 'Part 4: Todo API (WITHOUT signature verification)',
        'warning': '⚠️ This backend does NOT verify JWT signatures!',
        'note': 'This is for learning only. See example-part-5 for secure implementation.',
        'endpoints': {
            'GET /api/todos': 'Get todos (requires token)',
            'POST /api/todos': 'Create todo (requires token)',
            'PUT /api/todos/<id>/toggle': 'Toggle todo completion (requires token)',
            'DELETE /api/todos/<id>': 'Delete todo (requires token)'
        }
    })


@app.route('/api/todos', methods=['GET'])
@require_auth
def get_todos():
    """
    Get todos for the authenticated user
    - Regular users see only their own todos
    - Admin users see all todos
    """
    user_id = get_user_id()

    if is_admin():
        # Admin sees all todos
        return jsonify(todos)
    else:
        # Regular user sees only their todos
        user_todos = [t for t in todos if t['user_id'] == user_id]
        return jsonify(user_todos)


@app.route('/api/todos', methods=['POST'])
@require_auth
def create_todo():
    """Create a new todo for the authenticated user"""
    global todo_id_counter

    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing required field: text'}), 400

    text = data['text'].strip()
    if not text:
        return jsonify({'error': 'Todo text cannot be empty'}), 400

    user_id = get_user_id()
    username = get_username()

    new_todo = {
        'id': todo_id_counter,
        'text': text,
        'completed': False,
        'user_id': user_id,
        'username': username,
        'created_at': datetime.now().isoformat()
    }

    todos.append(new_todo)
    todo_id_counter += 1

    print(f"✓ Todo created by {username}: {text}")

    return jsonify(new_todo), 201


@app.route('/api/todos/<int:todo_id>/toggle', methods=['PUT'])
@require_auth
def toggle_todo(todo_id):
    """Toggle todo completion status"""
    user_id = get_user_id()

    # Find the todo
    todo = next((t for t in todos if t['id'] == todo_id), None)

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Check permissions: owner or admin
    if todo['user_id'] != user_id and not is_admin():
        return jsonify({'error': 'Forbidden: You can only toggle your own todos'}), 403

    # Toggle completion status
    todo['completed'] = not todo['completed']

    print(f"✓ Todo {todo_id} toggled by {get_username()}")

    return jsonify(todo)


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@require_auth
def delete_todo(todo_id):
    """Delete a todo"""
    global todos

    user_id = get_user_id()

    # Find the todo
    todo = next((t for t in todos if t['id'] == todo_id), None)

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Check permissions: owner or admin
    if todo['user_id'] != user_id and not is_admin():
        return jsonify({'error': 'Forbidden: You can only delete your own todos'}), 403

    # Delete the todo
    todos = [t for t in todos if t['id'] != todo_id]

    print(f"✓ Todo {todo_id} deleted by {get_username()}")

    return '', 204


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("Part 4 Example: Todo API WITHOUT Signature Verification")
    print("=" * 70)
    print("")
    print("⚠️  WARNING: This backend does NOT verify JWT signatures!")
    print("   Anyone can forge tokens and access the API.")
    print("   This is for LEARNING ONLY - DO NOT use in production!")
    print("")
    print("   For secure implementation with signature verification,")
    print("   see example-part-5-protected-api")
    print("")
    print("=" * 70)
    print("")
    print("API Endpoints:")
    print("  GET    /api/todos           - Get todos (auth required)")
    print("  POST   /api/todos           - Create todo (auth required)")
    print("  PUT    /api/todos/<id>/toggle - Toggle todo (auth required)")
    print("  DELETE /api/todos/<id>      - Delete todo (auth required)")
    print("")
    print("CORS enabled for:")
    print("  - http://localhost:3000")
    print("  - http://127.0.0.1:3000")
    print("")
    print("Server starting on http://localhost:5001")
    print("=" * 70)
    print("")

    app.run(debug=True, port=5001, host='0.0.0.0')
