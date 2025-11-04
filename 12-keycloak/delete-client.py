#!/usr/bin/env python3
"""
Keycloak Client Deletion Script
Deletes a client via Keycloak Admin REST API
"""

import requests
import sys
import urllib3

# SSL/TLS Configuration
INSECURE = True

if INSECURE:
    # Disable SSL warnings when using self-signed certificates
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration - CHANGE THESE VALUES
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-johan.se"
REALM = "myapp"
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin-change-this-password"

# Client to delete
CLIENT_ID = "my-frontend-app"


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


def delete_client(token, client_id):
    """Delete a client from Keycloak"""
    print(f"Step 2: Deleting client '{client_id}'...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Get client UUID
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients?clientId={client_id}"

    try:
        response = requests.get(url, headers=headers, verify=not INSECURE)
        response.raise_for_status()
        clients = response.json()

        if not clients:
            print(f"⚠️  Client '{client_id}' not found")
            return False

        client_uuid = clients[0]["id"]
        print(f"Found client with UUID: {client_uuid}")

        # Delete client
        delete_url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients/{client_uuid}"
        response = requests.delete(delete_url, headers=headers, verify=not INSECURE)

        if response.status_code == 204:
            print(f"✅ Client '{client_id}' deleted successfully\n")
            return True
        else:
            print(f"❌ Failed to delete client (HTTP {response.status_code})")
            print(response.text)
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


def main():
    print("=" * 40)
    print("Keycloak Client Deletion Script")
    print("=" * 40)
    print()

    # Get admin token
    token = get_admin_token()

    # Delete client
    success = delete_client(token, CLIENT_ID)

    if success:
        print("=" * 40)
        print("✅ Client deleted successfully!")
        print("=" * 40)
        print()
        print("You can now recreate it with:")
        print("  python3 create-client.py")
        print()
    else:
        print()
        print("Failed to delete client")
        sys.exit(1)


if __name__ == "__main__":
    main()
