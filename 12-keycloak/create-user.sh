#!/bin/bash

# Keycloak User Creation Script
# Automates user creation via Keycloak Admin REST API

# SSL/TLS Configuration
# Use INSECURE=true for staging/self-signed certificates
# Use INSECURE=false for production Let's Encrypt certificates
INSECURE=true
CURL_OPTS=$([ "$INSECURE" = "true" ] && echo "-k" || echo "")

# Configuration - CHANGE THESE VALUES
KEYCLOAK_URL="https://keycloak.ltu-m7011e-johan.se"
REALM="myapp"
ADMIN_USER="admin"
ADMIN_PASSWORD="admin-change-this-password"

# User details
USERNAME="testuser"
EMAIL="test@example.com"
FIRST_NAME="Test"
LAST_NAME="User"
PASSWORD="testpass123"

echo "========================================"
echo "Keycloak User Creation Script"
echo "========================================"
echo ""

# Get admin access token
echo "Step 1: Authenticating as admin..."
TOKEN=$(curl $CURL_OPTS -s -X POST "$KEYCLOAK_URL/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$ADMIN_USER" \
  -d "password=$ADMIN_PASSWORD" \
  -d "grant_type=password" \
  -d "client_id=admin-cli" \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Failed to get admin token. Check your credentials and Keycloak URL."
  exit 1
fi

echo "✅ Admin token obtained"
echo ""

# Create user
echo "Step 2: Creating user '$USERNAME'..."
RESPONSE=$(curl $CURL_OPTS -s -i -X POST "$KEYCLOAK_URL/admin/realms/$REALM/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$USERNAME\",
    \"email\": \"$EMAIL\",
    \"firstName\": \"$FIRST_NAME\",
    \"lastName\": \"$LAST_NAME\",
    \"enabled\": true,
    \"emailVerified\": true
  }")

# Extract user ID from Location header
USER_ID=$(echo "$RESPONSE" | grep -i "^location:" | sed 's/.*\///' | tr -d '\r\n')

if [ -z "$USER_ID" ]; then
  # Check if user already exists
  if echo "$RESPONSE" | grep -q "409"; then
    echo "⚠️  User '$USERNAME' already exists"
    exit 0
  else
    echo "❌ Failed to create user"
    echo "$RESPONSE"
    exit 1
  fi
fi

echo "✅ User created with ID: $USER_ID"
echo ""

# Set password
echo "Step 3: Setting password..."
curl $CURL_OPTS -s -X PUT "$KEYCLOAK_URL/admin/realms/$REALM/users/$USER_ID/reset-password" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"password\",
    \"value\": \"$PASSWORD\",
    \"temporary\": false
  }"

echo "✅ Password set successfully"
echo ""

echo "========================================"
echo "✅ User created successfully!"
echo "========================================"
echo ""
echo "Login credentials:"
echo "  Username: $USERNAME"
echo "  Password: $PASSWORD"
echo ""
echo "Test login at:"
echo "  $KEYCLOAK_URL/realms/$REALM/account"
echo ""
