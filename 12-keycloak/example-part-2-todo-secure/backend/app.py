#!/usr/bin/env python3
"""Part 2: Todo API with verified JWTs and owner-only authorization.
Todos are stored in memory; run one backend process until you add shared storage.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import os
import time
import requests
import urllib3
from functools import wraps
from datetime import datetime

app = Flask(__name__)

# Configure CORS to allow requests from React frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ] if not os.getenv("FRONTEND_URL") else [os.environ["FRONTEND_URL"]],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# SSL/TLS Configuration
# Use INSECURE=True for staging/self-signed certificates
# Use INSECURE=False for production Let's Encrypt certificates
INSECURE = os.getenv("INSECURE", "true").lower() == "true"

if INSECURE:
    # Disable SSL warnings when using self-signed certificates
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Keycloak configuration - UPDATE THESE VALUES
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "https://keycloak.ltu-m7011e-johan.se").rstrip("/")  # Change to your Keycloak URL
REALM = os.getenv("KEYCLOAK_REALM", "myapp")  # Change this to match your realm
CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "my-frontend-app")
API_AUDIENCE = os.getenv("KEYCLOAK_AUDIENCE", "todo-api")  # Audience mapper on the frontend client

# Keycloak endpoints
KEYCLOAK_ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"
KEYCLOAK_CERTS_URL = f"{KEYCLOAK_ISSUER}/protocol/openid-connect/certs"

# Cache public keys for five minutes; refresh once on an unknown signing key.
public_keys_cache = None
public_keys_fetched_at = 0.0

# In-memory storage for todos
# In production, use a proper database (PostgreSQL, etc.)
todos = []
todo_id_counter = 1


def get_public_keys(force_refresh=False):
    """
    Fetch public keys from Keycloak for JWT verification
    Keycloak uses these keys to sign JWTs - we use them to verify signatures
    """
    global public_keys_cache, public_keys_fetched_at

    if force_refresh or public_keys_cache is None or time.monotonic() - public_keys_fetched_at > 300:
        try:
            response = requests.get(KEYCLOAK_CERTS_URL, timeout=10, verify=not INSECURE)
            response.raise_for_status()
            public_keys_cache = response.json()
            public_keys_fetched_at = time.monotonic()
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

        # Refresh JWKS once for an unknown kid so key rotation is supported.
        key = next((key for key in keys['keys'] if key['kid'] == key_id), None)
        if key is None:
            keys = get_public_keys(force_refresh=True)
            key = next((key for key in keys['keys'] if key['kid'] == key_id), None)
        if key is None:
            raise jwt.InvalidTokenError("Unknown signing key")
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)

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
            audience=API_AUDIENCE,  # Audience mapper configured on the frontend client
            issuer=KEYCLOAK_ISSUER,
            options={
                'require': ['exp', 'iss', 'sub', 'aud'],
                'verify_signature': True,
                'verify_exp': True,
                'verify_nbf': True,
                'verify_iss': True,
                'verify_aud': True
            }
        )

        if not isinstance(decoded_token.get("sub"), str) or not decoded_token["sub"]:
            raise jwt.InvalidTokenError("Token requires a non-empty subject")

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

        except Exception as e:
            print(f"Authentication failed: {e}")
            return jsonify({'error': str(e)}), 401

        return f(*args, **kwargs)

    return decorated_function


def get_user_id():
    """Extract user ID from verified token"""
    return request.user.get('sub')


def get_username():
    """Extract username from verified token"""
    return request.user.get('preferred_username', 'unknown')




# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/')
def index():
    return jsonify({
        'message': 'Part 2: Todo API WITH signature verification (No RBAC)',
        'security': '✅ JWT signatures are verified',
        'note': 'No role-based access control - all users see their own todos',
        'endpoints': {
            'GET /api/todos': 'Get your todos',
            'POST /api/todos': 'Create todo',
            'PUT /api/todos/<id>/toggle': 'Toggle todo',
            'DELETE /api/todos/<id>': 'Delete todo'
        }
    })


@app.route('/api/todos', methods=['GET'])
@require_auth
def get_todos():
    """Get todos for current user only (no admin privileges)"""
    user_id = get_user_id()
    # Everyone sees only their own todos
    user_todos = [t for t in todos if t['user_id'] == user_id]
    return jsonify(user_todos)


@app.route('/api/todos', methods=['POST'])
@require_auth
def create_todo():
    """Create a new todo"""
    global todo_id_counter

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get('text'), str):
        return jsonify({'error': 'Missing or invalid required field: text'}), 400

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
    """Toggle todo completion - own todos only"""
    user_id = get_user_id()

    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Can only toggle own todos (no admin override)
    if todo['user_id'] != user_id:
        return jsonify({'error': 'Forbidden: You can only toggle your own todos'}), 403

    todo['completed'] = not todo['completed']
    return jsonify(todo)


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@require_auth
def delete_todo(todo_id):
    """Delete todo - own todos only"""
    global todos
    user_id = get_user_id()

    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Can only delete own todos (no admin override)
    if todo['user_id'] != user_id:
        return jsonify({'error': 'Forbidden: You can only delete your own todos'}), 403

    todos = [t for t in todos if t['id'] != todo_id]
    return '', 204


if __name__ == '__main__':
    print("=" * 70)
    print("Part 2 Example: Todo API WITH Signature Verification")
    print("=" * 70)
    print("")
    print("✅ JWT signatures are properly verified")
    print("✅ Uses Keycloak public keys for verification")
    print("✅ Validates expiration, issuer, audience")
    print("❌ No role-based access control (RBAC)")
    print("   All users can only see/edit their own todos")
    print("")
    print("For RBAC (admin can see all todos), see example-part-3-todo-rbac")
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
