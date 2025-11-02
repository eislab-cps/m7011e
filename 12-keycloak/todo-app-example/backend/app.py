#!/usr/bin/env python3
"""
Secure Todo API with Keycloak JWT authentication
This backend validates JWT tokens from Keycloak and implements role-based access control
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import requests
from functools import wraps
from datetime import datetime

app = Flask(__name__)

# Configure CORS to allow requests from React frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Keycloak configuration - UPDATE THESE VALUES
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-YOUR-NAME.se"  # Change to your Keycloak URL
REALM = "m7011e"
CLIENT_ID = "todo-app"

# Keycloak endpoints
KEYCLOAK_ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"
KEYCLOAK_CERTS_URL = f"{KEYCLOAK_ISSUER}/protocol/openid-connect/certs"

# Cache for public keys (in production, implement proper caching with expiration)
public_keys_cache = None

# In-memory storage for todos
# In production, use a proper database (PostgreSQL, etc.)
todos = []
todo_id_counter = 1


def get_public_keys():
    """
    Fetch public keys from Keycloak for JWT verification
    Keycloak uses these keys to sign JWTs - we use them to verify signatures
    """
    global public_keys_cache

    if public_keys_cache is None:
        try:
            response = requests.get(KEYCLOAK_CERTS_URL, timeout=10)
            response.raise_for_status()
            public_keys_cache = response.json()
            print(f"✓ Fetched public keys from Keycloak")
        except Exception as e:
            print(f"✗ Error fetching public keys: {e}")
            raise Exception("Failed to fetch Keycloak public keys")

    return public_keys_cache


def verify_token(token):
    """
    Verify JWT token from Keycloak
    Steps:
    1. Decode token header to get key ID (kid)
    2. Find matching public key from Keycloak
    3. Verify signature using public key
    4. Validate claims (expiration, issuer, audience)
    5. Return decoded token with user information
    """
    try:
        # Get public keys from Keycloak
        keys = get_public_keys()

        # Decode token header (without verification) to get key ID
        unverified_header = jwt.get_unverified_header(token)
        key_id = unverified_header.get('kid')

        if not key_id:
            raise Exception("Token missing key ID (kid)")

        # Find the matching public key
        public_key = None
        for key in keys['keys']:
            if key['kid'] == key_id:
                # Convert JWK to PEM format for PyJWT
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                break

        if not public_key:
            raise Exception(f"Public key not found for kid: {key_id}")

        # Verify and decode the token
        # This validates:
        # - Signature (ensures token was signed by Keycloak)
        # - Expiration (exp claim)
        # - Not before (nbf claim)
        # - Issuer (iss claim)
        # - Audience (aud claim)
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience='account',  # Keycloak sets this as default audience
            issuer=KEYCLOAK_ISSUER,
            options={
                'verify_signature': True,
                'verify_exp': True,
                'verify_nbf': True,
                'verify_iss': True,
                'verify_aud': True
            }
        )

        return decoded_token

    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError as e:
        raise Exception(f"Invalid token: {str(e)}")
    except Exception as e:
        raise Exception(f"Token verification failed: {str(e)}")


def require_auth(f):
    """
    Decorator to require authentication for endpoints
    Validates JWT token from Authorization header
    Adds decoded token to request.user for use in endpoint
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get Authorization header
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'error': 'No authorization header provided'}), 401

        # Extract token from "Bearer <token>" format
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Invalid authorization header format. Use: Bearer <token>'}), 401

        token = parts[1]

        try:
            # Verify token and extract user information
            decoded_token = verify_token(token)

            # Add user information to request context
            request.user = decoded_token

            # Continue to the actual endpoint
            return f(*args, **kwargs)

        except Exception as e:
            print(f"Authentication failed: {e}")
            return jsonify({'error': str(e)}), 401

    return decorated_function


def get_user_id():
    """Extract user ID from verified token"""
    return request.user.get('sub')


def get_username():
    """Extract username from verified token"""
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
        'message': 'Secure Todo API with Keycloak',
        'version': '1.0',
        'keycloak': {
            'url': KEYCLOAK_URL,
            'realm': REALM,
            'issuer': KEYCLOAK_ISSUER
        },
        'endpoints': {
            'GET /api/todos': 'Get todos (requires auth)',
            'POST /api/todos': 'Create todo (requires auth)',
            'PUT /api/todos/<id>/toggle': 'Toggle todo completion (requires auth)',
            'DELETE /api/todos/<id>': 'Delete todo (requires auth)'
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
    print("=" * 60)
    print("Starting Secure Todo API with Keycloak Authentication")
    print("=" * 60)
    print(f"Keycloak URL: {KEYCLOAK_URL}")
    print(f"Realm: {REALM}")
    print(f"Client ID: {CLIENT_ID}")
    print(f"Issuer: {KEYCLOAK_ISSUER}")
    print("")
    print("API Endpoints:")
    print("  GET    /api/todos           - Get todos (auth required)")
    print("  POST   /api/todos           - Create todo (auth required)")
    print("  PUT    /api/todos/<id>/toggle - Toggle todo (auth required)")
    print("  DELETE /api/todos/<id>      - Delete todo (auth required)")
    print("")
    print("CORS enabled for: http://localhost:3000")
    print("")
    print("Server starting on http://localhost:5000")
    print("=" * 60)
    print("")

    # Fetch public keys on startup to verify Keycloak connectivity
    try:
        get_public_keys()
    except Exception as e:
        print(f"WARNING: Could not fetch Keycloak public keys: {e}")
        print("Make sure Keycloak is running and the URL is correct!")
        print("")

    app.run(debug=True, port=5000, host='0.0.0.0')
