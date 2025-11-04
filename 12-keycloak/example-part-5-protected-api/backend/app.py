#!/usr/bin/env python3
"""
Part 5: Protected Flask API with JWT Validation
Demonstrates how to protect Flask endpoints with Keycloak JWT tokens
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
import requests
import urllib3
import json
from functools import wraps

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

# SSL/TLS Configuration
# Use INSECURE=True for staging/self-signed certificates
# Use INSECURE=False for production Let's Encrypt certificates
INSECURE = True

if INSECURE:
    # Disable SSL warnings when using self-signed certificates
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Keycloak configuration - UPDATE THIS
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-YOUR-NAME.se"
REALM = "myapp"
CERTS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

# Cache for public keys
public_keys = None

def get_public_keys():
    """Fetch public keys from Keycloak for token verification"""
    global public_keys
    if not public_keys:
        response = requests.get(CERTS_URL, verify=not INSECURE)
        public_keys = response.json()
    return public_keys

def require_auth(f):
    """Decorator to require valid JWT token"""
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
            # Decode and verify token
            keys = get_public_keys()
            unverified_header = jwt.get_unverified_header(token)

            # Find matching public key
            rsa_key = None
            for key in keys['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))

            if not rsa_key:
                return jsonify({'error': 'Public key not found'}), 401

            # Verify token signature and claims
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=['RS256'],
                audience='account',
                options={'verify_exp': True}
            )

            # Add user info to request context
            request.user = payload
            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'error': f'Invalid token: {str(e)}'}), 401

    return decorated_function

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'message': 'Part 5: Protected API with JWT',
        'keycloak_url': KEYCLOAK_URL,
        'realm': REALM
    })

@app.route('/api/public')
def public():
    """Public endpoint - no authentication required"""
    return jsonify({
        'message': 'This is public data - anyone can access this!'
    })

@app.route('/api/protected')
@require_auth
def protected():
    """Protected endpoint - requires valid token"""
    return jsonify({
        'message': 'This is protected data - you are authenticated!',
        'user': request.user['preferred_username'],
        'email': request.user.get('email', 'N/A'),
        'roles': request.user.get('realm_access', {}).get('roles', [])
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Part 5: Protected API with Keycloak JWT Validation")
    print("=" * 60)
    print(f"Keycloak URL: {KEYCLOAK_URL}")
    print(f"Realm: {REALM}")
    print("")
    print("API Endpoints:")
    print("  GET /              - Health check")
    print("  GET /api/public    - Public (no auth)")
    print("  GET /api/protected - Protected (requires JWT)")
    print("")
    print("Server starting on http://localhost:5001")
    print("=" * 60)
    print("")

    # Fetch public keys on startup
    try:
        get_public_keys()
        print("✓ Successfully fetched Keycloak public keys")
    except Exception as e:
        print(f"WARNING: Could not fetch Keycloak public keys: {e}")
        print("Make sure Keycloak is running!")
    print("")

    app.run(debug=True, port=5001, host='0.0.0.0')
