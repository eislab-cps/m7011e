#!/bin/bash

# Keycloak Realm Creation Script
# Automates realm creation via Keycloak Admin REST API

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

echo "========================================"
echo "Keycloak Realm Creation Script"
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

# Create realm
echo "Step 2: Creating realm '$REALM'..."
RESPONSE=$(curl $CURL_OPTS -s -w "\n%{http_code}" -X POST "$KEYCLOAK_URL/admin/realms" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"realm\": \"$REALM\",
    \"enabled\": true,
    \"displayName\": \"My Application Realm\",
    \"loginWithEmailAllowed\": true,
    \"duplicateEmailsAllowed\": false,
    \"resetPasswordAllowed\": true,
    \"editUsernameAllowed\": false,
    \"bruteForceProtected\": true
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "201" ]; then
  echo "✅ Realm '$REALM' created successfully"
elif [ "$HTTP_CODE" = "409" ]; then
  echo "⚠️  Realm '$REALM' already exists"
else
  echo "❌ Failed to create realm (HTTP $HTTP_CODE)"
  echo "$BODY"
  exit 1
fi

echo ""
echo "========================================"
echo "✅ Realm setup complete!"
echo "========================================"
echo ""
echo "Realm: $REALM"
echo "Realm URL: $KEYCLOAK_URL/realms/$REALM"
echo "Account Console: $KEYCLOAK_URL/realms/$REALM/account"
echo ""
echo "Next steps:"
echo "  1. Run ./create-user.sh to create users"
echo "  2. Create clients in the Keycloak Admin Console"
echo ""
