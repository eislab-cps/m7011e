#!/bin/bash

# Keycloak Client Creation Script
# Automates client/application creation via Keycloak Admin REST API

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

# Client configuration
CLIENT_ID="my-frontend-app"
CLIENT_NAME="My Frontend Application"
CLIENT_TYPE="public"  # "public" for frontend apps, "confidential" for backend APIs
ROOT_URL="http://localhost:3000"

echo "========================================"
echo "Keycloak Client Creation Script"
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

# Determine client authentication setting
if [ "$CLIENT_TYPE" = "confidential" ]; then
  PUBLIC_CLIENT="false"
  echo "Step 2: Creating confidential client '$CLIENT_ID' (backend/API)..."
else
  PUBLIC_CLIENT="true"
  echo "Step 2: Creating public client '$CLIENT_ID' (frontend)..."
fi

# Create client
RESPONSE=$(curl $CURL_OPTS -s -w "\n%{http_code}" -X POST "$KEYCLOAK_URL/admin/realms/$REALM/clients" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"clientId\": \"$CLIENT_ID\",
    \"name\": \"$CLIENT_NAME\",
    \"enabled\": true,
    \"publicClient\": $PUBLIC_CLIENT,
    \"protocol\": \"openid-connect\",
    \"rootUrl\": \"$ROOT_URL\",
    \"baseUrl\": \"$ROOT_URL\",
    \"redirectUris\": [\"$ROOT_URL/*\"],
    \"webOrigins\": [\"$ROOT_URL\"],
    \"standardFlowEnabled\": true,
    \"directAccessGrantsEnabled\": true,
    \"serviceAccountsEnabled\": $([ "$CLIENT_TYPE" = "confidential" ] && echo "true" || echo "false"),
    \"authorizationServicesEnabled\": false
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "201" ]; then
  echo "✅ Client '$CLIENT_ID' created successfully"
  echo ""

  # If confidential client, get the client secret
  if [ "$CLIENT_TYPE" = "confidential" ]; then
    echo "Step 3: Retrieving client secret..."

    # Get the client's internal ID
    CLIENT_UUID=$(curl $CURL_OPTS -s -X GET "$KEYCLOAK_URL/admin/realms/$REALM/clients?clientId=$CLIENT_ID" \
      -H "Authorization: Bearer $TOKEN" \
      | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)

    if [ -n "$CLIENT_UUID" ]; then
      # Get client secret
      CLIENT_SECRET=$(curl $CURL_OPTS -s -X GET "$KEYCLOAK_URL/admin/realms/$REALM/clients/$CLIENT_UUID/client-secret" \
        -H "Authorization: Bearer $TOKEN" \
        | grep -o '"value":"[^"]*' | cut -d'"' -f4)

      if [ -n "$CLIENT_SECRET" ]; then
        echo "✅ Client secret retrieved"
        echo ""
        echo "========================================"
        echo "⚠️  SAVE THIS SECRET - IT WON'T BE SHOWN AGAIN!"
        echo "========================================"
        echo "Client ID: $CLIENT_ID"
        echo "Client Secret: $CLIENT_SECRET"
        echo ""
      fi
    fi
  fi

elif [ "$HTTP_CODE" = "409" ]; then
  echo "⚠️  Client '$CLIENT_ID' already exists"
else
  echo "❌ Failed to create client (HTTP $HTTP_CODE)"
  echo "$BODY"
  exit 1
fi

echo ""
echo "========================================"
echo "✅ Client setup complete!"
echo "========================================"
echo ""
echo "Client ID: $CLIENT_ID"
echo "Client Type: $CLIENT_TYPE"
echo "Root URL: $ROOT_URL"
echo "Valid Redirect URIs: $ROOT_URL/*"
echo "Web Origins: $ROOT_URL"
echo ""
echo "Use this client in your application:"
if [ "$CLIENT_TYPE" = "public" ]; then
  echo "  - Frontend (React, Vue, etc.)"
  echo "  - Client ID: $CLIENT_ID"
  echo "  - No client secret needed (public client)"
else
  echo "  - Backend API (Flask, Express, etc.)"
  echo "  - Client ID: $CLIENT_ID"
  echo "  - Client Secret: (saved above)"
fi
echo ""
