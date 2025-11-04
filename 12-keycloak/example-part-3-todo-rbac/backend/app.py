#!/usr/bin/env python3
"""
Part 3 Example: Todo API WITH RBAC (Role-Based Access Control)
This backend properly verifies JWT signatures AND implements role-based access.
- Admin users can see and manage ALL todos
- Regular users can only see and manage their OWN todos
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import requests
import urllib3
import json
from functools import wraps
from datetime import datetime

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# SSL Configuration
INSECURE = True
if INSECURE:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Keycloak configuration
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-johan.se"
REALM = "myapp"
CERTS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

# Cache for public keys
public_keys = None

# In-memory storage
todos = []
todo_id_counter = 1


def get_public_keys():
    """Fetch public keys from Keycloak"""
    global public_keys
    if not public_keys:
        response = requests.get(CERTS_URL, verify=not INSECURE)
        public_keys = response.json()
    return public_keys


def require_auth(f):
    """Decorator WITH signature verification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Invalid authorization header'}), 401

        token = parts[1]

        try:
            # ✅ SECURE: Verify signature using Keycloak public keys
            keys = get_public_keys()
            unverified_header = jwt.get_unverified_header(token)

            rsa_key = None
            for key in keys['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))

            if not rsa_key:
                return jsonify({'error': 'Public key not found'}), 401

            # Verify signature and validate claims
            decoded_token = jwt.decode(
                token,
                rsa_key,
                algorithms=['RS256'],
                audience='account',
                options={
                    'verify_signature': True,  # ✅ Verify signature!
                    'verify_exp': True,
                    'verify_nbf': True,
                    'verify_iss': True,
                    'verify_aud': True
                }
            )

            request.user = decoded_token
            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'error': f'Invalid token: {str(e)}'}), 401

    return decorated_function


def get_user_id():
    return request.user.get('sub')


def get_username():
    return request.user.get('preferred_username', 'unknown')


def is_admin():
    """Check if the authenticated user has admin role"""
    realm_roles = request.user.get('realm_access', {}).get('roles', [])
    return 'admin' in realm_roles


# =============================================================================
# API ENDPOINTS WITH RBAC
# =============================================================================

@app.route('/')
def index():
    return jsonify({
        'message': 'Part 3: Todo API WITH RBAC',
        'security': '✅ JWT signatures are verified',
        'rbac': '✅ Role-based access control enabled',
        'roles': {
            'admin': 'Can view and manage ALL todos',
            'user': 'Can only view and manage OWN todos'
        },
        'endpoints': {
            'GET /api/todos': 'Get todos (all for admin, own for users)',
            'POST /api/todos': 'Create todo',
            'PUT /api/todos/<id>/toggle': 'Toggle todo (own only, or admin)',
            'DELETE /api/todos/<id>': 'Delete todo (own only, or admin)'
        }
    })


@app.route('/api/todos', methods=['GET'])
@require_auth
def get_todos():
    """Get todos - admin sees ALL, users see only their own"""
    if is_admin():
        # Admin can see all todos
        return jsonify(todos)
    else:
        # Regular users see only their own todos
        user_id = get_user_id()
        user_todos = [t for t in todos if t['user_id'] == user_id]
        return jsonify(user_todos)


@app.route('/api/todos', methods=['POST'])
@require_auth
def create_todo():
    """Create a new todo"""
    global todo_id_counter

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing required field: text'}), 400

    text = data['text'].strip()
    if not text:
        return jsonify({'error': 'Todo text cannot be empty'}), 400

    new_todo = {
        'id': todo_id_counter,
        'text': text,
        'completed': False,
        'user_id': get_user_id(),
        'username': get_username(),
        'created_at': datetime.now().isoformat()
    }

    todos.append(new_todo)
    todo_id_counter += 1

    return jsonify(new_todo), 201


@app.route('/api/todos/<int:todo_id>/toggle', methods=['PUT'])
@require_auth
def toggle_todo(todo_id):
    """Toggle todo completion - own todos only, or admin can toggle any"""
    user_id = get_user_id()

    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Admin can toggle any todo, regular users can only toggle their own
    if not is_admin() and todo['user_id'] != user_id:
        return jsonify({'error': 'Forbidden: You can only toggle your own todos'}), 403

    todo['completed'] = not todo['completed']
    return jsonify(todo)


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@require_auth
def delete_todo(todo_id):
    """Delete todo - own todos only, or admin can delete any"""
    global todos
    user_id = get_user_id()

    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Admin can delete any todo, regular users can only delete their own
    if not is_admin() and todo['user_id'] != user_id:
        return jsonify({'error': 'Forbidden: You can only delete your own todos'}), 403

    todos = [t for t in todos if t['id'] != todo_id]
    return '', 204


if __name__ == '__main__':
    print("=" * 70)
    print("Part 3 Example: Todo API WITH RBAC")
    print("=" * 70)
    print("")
    print("✅ JWT signatures are properly verified")
    print("✅ Uses Keycloak public keys for verification")
    print("✅ Role-Based Access Control (RBAC) enabled")
    print("")
    print("Roles:")
    print("  👑 admin - Can view/edit ALL todos")
    print("  👤 user  - Can only view/edit OWN todos")
    print("")
    print("=" * 70)
    print("")

    try:
        get_public_keys()
        print("✓ Successfully fetched Keycloak public keys")
    except Exception as e:
        print(f"WARNING: Could not fetch public keys: {e}")
    print("")

    app.run(debug=True, port=5001, host='0.0.0.0')
