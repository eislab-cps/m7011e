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

### Step 1: Create Realm

1. In Keycloak Admin Console, click the dropdown in the top-left (shows "master")
2. Click **"Create Realm"**
3. Fill in:
   - Realm name: `myapp`
   - Enabled: ON
4. Click **"Create"**

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

### Step 1: Create a Public Client (for Frontend Apps)

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

**Problem**: Client not configured with correct redirect URI.

**Solution**:
1. Go to Clients → Your client
2. Check "Valid Redirect URIs" includes your app URL
3. Use `http://localhost:3000/*` for development
4. Use `https://yourdomain.com/*` for production

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

## Understanding the Technology (Optional Deep Dive)

### OAuth 2.0 vs OpenID Connect vs JWT

**OAuth 2.0** = Authorization framework ("what can you access?")
- Delegates access to resources
- Used by "Sign in with Google" buttons

**OpenID Connect (OIDC)** = Authentication layer on OAuth 2.0 ("who are you?")
- Adds user identity verification
- Provides ID tokens with user info

**JWT** = Token format
- Self-contained tokens with claims
- Cryptographically signed
- Used for both ID tokens and access tokens

**Keycloak implements all three!**

### Authentication Flow

```
1. User clicks "Login" in your app
2. App redirects to Keycloak login page
3. User enters credentials
4. Keycloak verifies credentials
5. Keycloak redirects back with authorization code
6. App exchanges code for tokens (access, ID, refresh)
7. App uses access token to call APIs
8. APIs verify token signature with Keycloak's public keys
```

### JWT Token Structure

A JWT has three parts: `header.payload.signature`

**Header**: Algorithm used
```json
{"alg": "RS256", "typ": "JWT"}
```

**Payload**: User info and claims
```json
{
  "sub": "user-id-123",
  "name": "Test User",
  "email": "test@example.com",
  "realm_access": {"roles": ["editor"]},
  "exp": 1735689600
}
```

**Signature**: Cryptographic signature
- Ensures token hasn't been tampered with
- Only Keycloak can create valid signatures
- Anyone can verify using Keycloak's public keys

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
- Deploy with Argo CD from Tutorial 11

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
