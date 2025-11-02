# Example Flask application with Keycloak authentication
# Install: pip install flask flask-cors pyjwt cryptography requests

from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import jwt
import requests
from functools import wraps
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Keycloak configuration
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-YOUR-NAME.se"
REALM = "m7011e"
CLIENT_ID = "demo-api"
CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"  # Get from Keycloak admin console

# Keycloak endpoints
KEYCLOAK_ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"
KEYCLOAK_CERTS_URL = f"{KEYCLOAK_ISSUER}/protocol/openid-connect/certs"
KEYCLOAK_TOKEN_URL = f"{KEYCLOAK_ISSUER}/protocol/openid-connect/token"
KEYCLOAK_USERINFO_URL = f"{KEYCLOAK_ISSUER}/protocol/openid-connect/userinfo"

# Cache for public keys
public_keys = None

def get_public_keys():
    """Fetch public keys from Keycloak for token verification"""
    global public_keys
    if public_keys is None:
        response = requests.get(KEYCLOAK_CERTS_URL)
        public_keys = response.json()
    return public_keys

def verify_token(token):
    """Verify JWT token from Keycloak"""
    try:
        # Get public keys
        keys = get_public_keys()

        # Decode token header to get key ID
        unverified_header = jwt.get_unverified_header(token)
        key_id = unverified_header.get('kid')

        # Find matching public key
        public_key = None
        for key in keys['keys']:
            if key['kid'] == key_id:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                break

        if not public_key:
            raise Exception("Public key not found")

        # Verify and decode token
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience='account',
            issuer=KEYCLOAK_ISSUER
        )

        return decoded_token
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError as e:
        raise Exception(f"Invalid token: {str(e)}")

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401

        try:
            # Extract token (format: "Bearer TOKEN")
            token = auth_header.split(' ')[1]

            # Verify token
            decoded_token = verify_token(token)

            # Add user info to request context
            request.user = decoded_token

            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 401

    return decorated_function

def require_role(role):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated_function(*args, **kwargs):
            # Check realm roles
            realm_roles = request.user.get('realm_access', {}).get('roles', [])

            # Check client roles
            client_roles = request.user.get('resource_access', {}).get(CLIENT_ID, {}).get('roles', [])

            if role not in realm_roles and role not in client_roles:
                return jsonify({'error': f'Role {role} required'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Public endpoint
@app.route('/')
def index():
    return jsonify({
        'message': 'Keycloak Flask API',
        'version': '1.0',
        'endpoints': {
            '/': 'Public endpoint',
            '/protected': 'Protected endpoint (requires authentication)',
            '/admin': 'Admin endpoint (requires admin role)',
            '/user-info': 'Get current user information',
            '/token': 'Get token using client credentials'
        }
    })

# Protected endpoint
@app.route('/protected')
@require_auth
def protected():
    return jsonify({
        'message': 'This is a protected endpoint',
        'user': {
            'id': request.user.get('sub'),
            'username': request.user.get('preferred_username'),
            'email': request.user.get('email'),
            'name': request.user.get('name')
        }
    })

# Admin-only endpoint
@app.route('/admin')
@require_role('admin')
def admin_only():
    return jsonify({
        'message': 'Admin access granted',
        'user': request.user.get('preferred_username'),
        'roles': request.user.get('realm_access', {}).get('roles', [])
    })

# Get user information
@app.route('/user-info')
@require_auth
def user_info():
    return jsonify({
        'user': {
            'id': request.user.get('sub'),
            'username': request.user.get('preferred_username'),
            'email': request.user.get('email'),
            'email_verified': request.user.get('email_verified'),
            'name': request.user.get('name'),
            'given_name': request.user.get('given_name'),
            'family_name': request.user.get('family_name'),
            'realm_roles': request.user.get('realm_access', {}).get('roles', []),
            'client_roles': request.user.get('resource_access', {}).get(CLIENT_ID, {}).get('roles', [])
        },
        'token_info': {
            'issued_at': datetime.fromtimestamp(request.user.get('iat')).isoformat(),
            'expires_at': datetime.fromtimestamp(request.user.get('exp')).isoformat(),
            'issuer': request.user.get('iss')
        }
    })

# Service-to-service authentication using client credentials
@app.route('/token')
def get_service_token():
    """Example: Get access token using client credentials flow"""
    try:
        response = requests.post(
            KEYCLOAK_TOKEN_URL,
            data={
                'grant_type': 'client_credentials',
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET
            }
        )

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to get token'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Example: Call another service with token
@app.route('/call-service')
@require_auth
def call_service():
    """Example: Make authenticated call to another service"""
    try:
        # Get our service token
        token_response = requests.post(
            KEYCLOAK_TOKEN_URL,
            data={
                'grant_type': 'client_credentials',
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET
            }
        )

        if token_response.status_code != 200:
            return jsonify({'error': 'Failed to get service token'}), 500

        service_token = token_response.json()['access_token']

        # Call another service (example)
        # service_response = requests.get(
        #     'https://other-service.example.com/api',
        #     headers={'Authorization': f'Bearer {service_token}'}
        # )

        return jsonify({
            'message': 'Service call example',
            'note': 'Uncomment the code above to call a real service',
            'service_token': service_token[:50] + '...'  # Show partial token
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print(f"Starting Flask API with Keycloak authentication")
    print(f"Keycloak URL: {KEYCLOAK_URL}")
    print(f"Realm: {REALM}")
    print(f"Client ID: {CLIENT_ID}")
    print(f"\nEndpoints:")
    print(f"  GET  /              - Public endpoint")
    print(f"  GET  /protected     - Protected endpoint (requires auth)")
    print(f"  GET  /admin         - Admin endpoint (requires admin role)")
    print(f"  GET  /user-info     - Get current user info")
    print(f"  GET  /token         - Get service token")
    print(f"  GET  /call-service  - Example service-to-service call")
    print(f"  GET  /health        - Health check")
    print(f"\nServer running on http://localhost:5000")

    app.run(debug=True, port=5000)
