#!/usr/bin/env python3
"""
Keycloak Client Creation Script
Automates client/application creation via Keycloak Admin REST API
"""

import requests
import sys
import urllib3

# SSL/TLS Configuration
# Use INSECURE=True for staging/self-signed certificates
# Use INSECURE=False for production Let's Encrypt certificates
INSECURE = True

if INSECURE:
    # Disable SSL warnings when using self-signed certificates
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - CHANGE THESE VALUES
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-johan.se"
REALM = "myapp"
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin-change-this-password"

# Client configuration
CLIENT_ID = "my-frontend-app"
CLIENT_NAME = "My Frontend Application"
CLIENT_TYPE = "public"  # "public" for frontend apps, "confidential" for backend APIs

# Frontend URLs - Add all URLs where your frontend might be accessed
# This is needed because OAuth redirect URIs must match exactly
FRONTEND_URLS = [
    "http://localhost:3000",      # Standard localhost
    "http://127.0.0.1:3000",      # IPv4 loopback
]
ROOT_URL = FRONTEND_URLS[0]  # Primary URL


def get_admin_token():
    """Get admin access token from Keycloak"""
    print("Step 1: Authenticating as admin...")

    url = f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
    data = {
        "username": ADMIN_USER,
        "password": ADMIN_PASSWORD,
        "grant_type": "password",
        "client_id": "admin-cli"
    }

    try:
        response = requests.post(url, data=data, verify=not INSECURE)
        response.raise_for_status()
        print("✅ Admin token obtained\n")
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get admin token: {e}")
        print("Check your credentials and Keycloak URL.")
        sys.exit(1)


def create_client(token, client_id, client_name, client_type, root_url):
    """Create a new client in Keycloak"""
    client_type_name = "confidential" if client_type == "confidential" else "public"
    app_type = "backend/API" if client_type == "confidential" else "frontend"

    print(f"Step 2: Creating {client_type_name} client '{client_id}' ({app_type})...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Build redirect URIs and web origins from FRONTEND_URLS
    redirect_uris = [f"{url}/*" for url in FRONTEND_URLS]
    web_origins = FRONTEND_URLS.copy()

    client_data = {
        "clientId": client_id,
        "name": client_name,
        "enabled": True,
        "publicClient": client_type != "confidential",
        "protocol": "openid-connect",
        "rootUrl": root_url,
        "baseUrl": root_url,
        "redirectUris": redirect_uris,
        "webOrigins": web_origins,
        "standardFlowEnabled": True,
        "directAccessGrantsEnabled": True,
        "serviceAccountsEnabled": client_type == "confidential",
        "authorizationServicesEnabled": False
    }

    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients"

    try:
        response = requests.post(url, json=client_data, headers=headers, verify=not INSECURE)

        if response.status_code == 201:
            print(f"✅ Client '{client_id}' created successfully\n")

            # If confidential client, get the client secret
            if client_type == "confidential":
                secret = get_client_secret(token, client_id, headers)
                return secret
            return None

        elif response.status_code == 409:
            print(f"⚠️  Client '{client_id}' already exists\n")
            return None
        else:
            print(f"❌ Failed to create client (HTTP {response.status_code})")
            print(response.text)
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)


def get_client_secret(token, client_id, headers):
    """Get the client secret for a confidential client"""
    print("Step 3: Retrieving client secret...")

    try:
        # Get the client's internal UUID
        url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients?clientId={client_id}"
        response = requests.get(url, headers=headers, verify=not INSECURE)
        response.raise_for_status()

        clients = response.json()
        if not clients:
            print("❌ Client not found")
            return None

        client_uuid = clients[0]["id"]

        # Get client secret
        secret_url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients/{client_uuid}/client-secret"
        secret_response = requests.get(secret_url, headers=headers, verify=not INSECURE)
        secret_response.raise_for_status()

        client_secret = secret_response.json()["value"]
        print("✅ Client secret retrieved\n")

        print("=" * 40)
        print("⚠️  SAVE THIS SECRET - IT WON'T BE SHOWN AGAIN!")
        print("=" * 40)
        print(f"Client ID: {client_id}")
        print(f"Client Secret: {client_secret}")
        print()

        return client_secret

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get client secret: {e}")
        return None


def main():
    print("=" * 40)
    print("Keycloak Client Creation Script")
    print("=" * 40)
    print()

    # Get admin token
    token = get_admin_token()

    # Create client
    secret = create_client(token, CLIENT_ID, CLIENT_NAME, CLIENT_TYPE, ROOT_URL)

    print()
    print("=" * 40)
    print("✅ Client setup complete!")
    print("=" * 40)
    print()
    print(f"Client ID: {CLIENT_ID}")
    print(f"Client Type: {CLIENT_TYPE}")
    print(f"Root URL: {ROOT_URL}")
    print()
    print("Valid Redirect URIs:")
    for url in FRONTEND_URLS:
        print(f"  - {url}/*")
    print()
    print("Web Origins:")
    for url in FRONTEND_URLS:
        print(f"  - {url}")
    print()
    print("Use this client in your application:")
    if CLIENT_TYPE == "public":
        print("  - Frontend (React, Vue, etc.)")
        print(f"  - Client ID: {CLIENT_ID}")
        print("  - No client secret needed (public client)")
        print()
        print("Access your frontend at any of these URLs:")
        for url in FRONTEND_URLS:
            print(f"  - {url}")
    else:
        print("  - Backend API (Flask, Express, etc.)")
        print(f"  - Client ID: {CLIENT_ID}")
        if secret:
            print(f"  - Client Secret: (saved above)")
    print()


if __name__ == "__main__":
    main()
