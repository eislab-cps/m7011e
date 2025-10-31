# Quick Start Guide

Follow these steps to get the todo app running locally with Keycloak authentication.

## Prerequisites Checklist

- [ ] Keycloak is deployed and accessible
- [ ] Realm `m7011e` is created in Keycloak
- [ ] Client `todo-app` is configured
- [ ] Test users are created (admin and regular user)
- [ ] Node.js and npm are installed
- [ ] Python 3.7+ is installed

## Step 1: Configure Keycloak Connection

### Frontend Configuration

Edit `frontend/src/keycloak-config.js`:

```javascript
export const keycloakConfig = {
  url: 'https://keycloak.ltu-m7011e-YOUR-NAME.se',  // <- Change this!
  realm: 'm7011e',
  clientId: 'todo-app'
};
```

### Backend Configuration

Edit `backend/app.py` (around line 25):

```python
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-YOUR-NAME.se"  # <- Change this!
REALM = "m7011e"
CLIENT_ID = "todo-app"
```

## Step 2: Start the Backend

### Option A: Using the script (recommended)

```bash
chmod +x start-backend.sh
./start-backend.sh
```

### Option B: Manual start

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

You should see:
```
Starting Secure Todo API with Keycloak Authentication
✓ Fetched public keys from Keycloak
Server starting on http://localhost:5000
```

**Keep this terminal open!**

## Step 3: Start the Frontend

Open a **new terminal window**.

### Option A: Using the script (recommended)

```bash
chmod +x start-frontend.sh
./start-frontend.sh
```

### Option B: Manual start

```bash
cd frontend
npm install
npm start
```

The browser should automatically open to `http://localhost:3000`

## Step 4: Test the Application

### Test 1: Login as Regular User

1. You'll be redirected to Keycloak login
2. Login with:
   - Username: `alice`
   - Password: `alice123`
3. You should see the todo interface
4. Add a todo: "Test alice's todo"
5. The todo is saved

### Test 2: Login as Admin

1. Click "Logout"
2. Login with:
   - Username: `admin`
   - Password: `admin123`
3. Add a todo: "Test admin todo"
4. You should see **both alice's and admin's todos** (admin sees all)
5. Notice the "Admin" badge in the header

### Test 3: Verify Token Authentication

1. Open browser developer tools (F12)
2. Go to Network tab
3. Add a new todo
4. Click on the POST request to `/api/todos`
5. Check the Headers section
6. You should see: `Authorization: Bearer eyJhbGci...`

### Test 4: Copy and Decode Token

1. In the app, scroll down to "User Information"
2. Expand "View Access Token"
3. Click "Decode at jwt.io"
4. You'll see the token structure with:
   - User ID (sub)
   - Username (preferred_username)
   - Roles (realm_access.roles)
   - Expiration (exp)

## Troubleshooting

### Problem: "Failed to fetch Keycloak public keys"

**Solution:**
- Check that Keycloak URL is correct in `backend/app.py`
- Ensure Keycloak is running and accessible
- Try accessing the URL in your browser:
  `https://keycloak.ltu-m7011e-YOUR-NAME.se/realms/m7011e`

### Problem: "Invalid redirect URI" error

**Solution:**
- In Keycloak admin console, go to Clients → todo-app
- Ensure "Valid redirect URIs" includes: `http://localhost:3000/*`
- Ensure "Web origins" includes: `http://localhost:3000`
- Save and try again

### Problem: CORS error in browser console

**Solution:**
- Ensure backend is running on port 5000
- Check that Flask-CORS is installed: `pip install flask-cors`
- Verify CORS configuration in `backend/app.py` allows `http://localhost:3000`

### Problem: "Connection refused" when adding todo

**Solution:**
- Check that backend is running: `curl http://localhost:5000`
- Ensure no firewall is blocking port 5000
- Check backend terminal for error messages

### Problem: Frontend won't start - "Port 3000 already in use"

**Solution:**
```bash
# Kill process on port 3000
# macOS/Linux:
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

## Next Steps

Once everything works:

1. Try the exercises in the main README
2. Add more features (todo editing, categories, etc.)
3. Deploy to Kubernetes
4. Add PostgreSQL database
5. Implement social login
6. Enable multi-factor authentication

## Support

If you encounter issues:

1. Check the browser console for errors (F12)
2. Check the backend terminal for error messages
3. Verify Keycloak configuration
4. Review the main README.md for detailed troubleshooting
