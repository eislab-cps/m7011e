"""
User Service - Example Flask service for AI documentation tutorial

This service demonstrates a typical microservice with:
- User registration and authentication
- Password hashing with bcrypt
- JWT token generation
- PostgreSQL database
- Redis caching
- Health checks
- Prometheus metrics

Perfect for demonstrating AI-powered documentation generation!
"""

from flask import Flask, request, jsonify
import psycopg2
import redis
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from prometheus_client import Counter, Histogram, generate_latest
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'dev-secret-key')

# Database connection
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'userdb'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'port': os.getenv('DB_PORT', '5432')
}

# Redis connection
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Prometheus metrics
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
http_request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
user_registrations_total = Counter('user_registrations_total', 'Total user registrations')
user_logins_total = Counter('user_logins_total', 'Total user login attempts', ['status'])

def get_db_connection():
    """Get PostgreSQL database connection"""
    return psycopg2.connect(**DB_CONFIG)

def require_auth(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'No token provided'}), 401

        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]

            # Verify token
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = payload['user_id']
            request.email = payload['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated_function

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check database
        conn = get_db_connection()
        conn.close()

        # Check Redis
        redis_client.ping()

        return jsonify({
            'status': 'healthy',
            'service': 'user-service',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

@app.route('/api/users/register', methods=['POST'])
def register_user():
    """
    Register a new user

    Request body:
    {
        "email": "user@example.com",
        "password": "securepassword",
        "name": "John Doe"
    }

    Returns:
    {
        "user_id": 123,
        "email": "user@example.com",
        "name": "John Doe",
        "created_at": "2024-01-15T10:30:00"
    }
    """
    with http_request_duration.labels(method='POST', endpoint='/api/users/register').time():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            name = data.get('name')

            # Validate input
            if not email or not password:
                http_requests_total.labels(method='POST', endpoint='/register', status='400').inc()
                return jsonify({'error': 'Email and password required'}), 400

            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Insert into database
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (email, password_hash, name, created_at)
                VALUES (%s, %s, %s, %s)
                RETURNING user_id, created_at
                """,
                (email, password_hash, name, datetime.utcnow())
            )

            user_id, created_at = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()

            # Cache user data
            cache_key = f"user:{user_id}"
            redis_client.setex(
                cache_key,
                3600,  # 1 hour TTL
                f"{email}|{name}"
            )

            user_registrations_total.inc()
            http_requests_total.labels(method='POST', endpoint='/register', status='201').inc()

            return jsonify({
                'user_id': user_id,
                'email': email,
                'name': name,
                'created_at': created_at.isoformat()
            }), 201

        except psycopg2.IntegrityError:
            http_requests_total.labels(method='POST', endpoint='/register', status='409').inc()
            return jsonify({'error': 'Email already exists'}), 409
        except Exception as e:
            http_requests_total.labels(method='POST', endpoint='/register', status='500').inc()
            return jsonify({'error': str(e)}), 500

@app.route('/api/users/login', methods=['POST'])
def login_user():
    """
    Login user and generate JWT token

    Request body:
    {
        "email": "user@example.com",
        "password": "securepassword"
    }

    Returns:
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user_id": 123,
        "email": "user@example.com",
        "expires_at": "2024-01-16T10:30:00"
    }
    """
    with http_request_duration.labels(method='POST', endpoint='/api/users/login').time():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                user_logins_total.labels(status='invalid_input').inc()
                return jsonify({'error': 'Email and password required'}), 400

            # Query database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, password_hash, name FROM users WHERE email = %s",
                (email,)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if not result:
                user_logins_total.labels(status='user_not_found').inc()
                return jsonify({'error': 'Invalid credentials'}), 401

            user_id, password_hash, name = result

            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                user_logins_total.labels(status='invalid_password').inc()
                return jsonify({'error': 'Invalid credentials'}), 401

            # Generate JWT token
            expires_at = datetime.utcnow() + timedelta(hours=24)
            token = jwt.encode(
                {
                    'user_id': user_id,
                    'email': email,
                    'name': name,
                    'exp': expires_at
                },
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )

            user_logins_total.labels(status='success').inc()
            http_requests_total.labels(method='POST', endpoint='/login', status='200').inc()

            return jsonify({
                'token': token,
                'user_id': user_id,
                'email': email,
                'name': name,
                'expires_at': expires_at.isoformat()
            }), 200

        except Exception as e:
            user_logins_total.labels(status='error').inc()
            return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """
    Get user information by ID (requires authentication)

    Headers:
    Authorization: Bearer <jwt-token>

    Returns:
    {
        "user_id": 123,
        "email": "user@example.com",
        "name": "John Doe",
        "created_at": "2024-01-15T10:30:00"
    }
    """
    with http_request_duration.labels(method='GET', endpoint='/api/users/:id').time():
        try:
            # Check cache first
            cache_key = f"user:{user_id}"
            cached_data = redis_client.get(cache_key)

            if cached_data:
                email, name = cached_data.split('|')
                return jsonify({
                    'user_id': user_id,
                    'email': email,
                    'name': name,
                    'source': 'cache'
                }), 200

            # Query database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT email, name, created_at FROM users WHERE user_id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if not result:
                http_requests_total.labels(method='GET', endpoint='/users', status='404').inc()
                return jsonify({'error': 'User not found'}), 404

            email, name, created_at = result

            # Update cache
            redis_client.setex(cache_key, 3600, f"{email}|{name}")

            http_requests_total.labels(method='GET', endpoint='/users', status='200').inc()

            return jsonify({
                'user_id': user_id,
                'email': email,
                'name': name,
                'created_at': created_at.isoformat(),
                'source': 'database'
            }), 200

        except Exception as e:
            http_requests_total.labels(method='GET', endpoint='/users', status='500').inc()
            return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@require_auth
def update_user(user_id):
    """
    Update user information (requires authentication)

    Headers:
    Authorization: Bearer <jwt-token>

    Request body:
    {
        "name": "Jane Doe"
    }

    Returns:
    {
        "user_id": 123,
        "email": "user@example.com",
        "name": "Jane Doe",
        "updated_at": "2024-01-15T11:30:00"
    }
    """
    # Verify user can only update their own profile
    if request.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        data = request.get_json()
        name = data.get('name')

        if not name:
            return jsonify({'error': 'Name required'}), 400

        # Update database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET name = %s, updated_at = %s
            WHERE user_id = %s
            RETURNING email, updated_at
            """,
            (name, datetime.utcnow(), user_id)
        )
        email, updated_at = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        # Invalidate cache
        cache_key = f"user:{user_id}"
        redis_client.delete(cache_key)

        return jsonify({
            'user_id': user_id,
            'email': email,
            'name': name,
            'updated_at': updated_at.isoformat()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize database schema
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database initialization failed: {e}")

    # Start server
    print("User Service starting...")
    print(f"Database: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    print(f"Redis: {REDIS_HOST}:{REDIS_PORT}")
    app.run(host='0.0.0.0', port=5000, debug=True)
