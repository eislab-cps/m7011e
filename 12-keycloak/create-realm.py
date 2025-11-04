#!/usr/bin/env python3
"""
Keycloak Realm Creation Script
Automates realm creation via Keycloak Admin REST API
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


def create_realm(token, realm_name):
    """Create a new realm in Keycloak"""
    print(f"Step 2: Creating realm '{realm_name}'...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    realm_data = {
        "realm": realm_name,
        "enabled": True,
        "displayName": "My Application Realm",
        "loginWithEmailAllowed": True,
        "duplicateEmailsAllowed": False,
        "resetPasswordAllowed": True,
        "editUsernameAllowed": False,
        "bruteForceProtected": True
    }

    url = f"{KEYCLOAK_URL}/admin/realms"

    try:
        response = requests.post(url, json=realm_data, headers=headers, verify=not INSECURE)

        if response.status_code == 201:
            print(f"✅ Realm '{realm_name}' created successfully\n")
            return True
        elif response.status_code == 409:
            print(f"⚠️  Realm '{realm_name}' already exists\n")
            return True
        else:
            print(f"❌ Failed to create realm (HTTP {response.status_code})")
            print(response.text)
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)


def main():
    print("=" * 40)
    print("Keycloak Realm Creation Script")
    print("=" * 40)
    print()

    # Get admin token
    token = get_admin_token()

    # Create realm
    create_realm(token, REALM)

    print("=" * 40)
    print("✅ Realm setup complete!")
    print("=" * 40)
    print()
    print(f"Realm: {REALM}")
    print(f"Realm URL: {KEYCLOAK_URL}/realms/{REALM}")
    print(f"Account Console: {KEYCLOAK_URL}/realms/{REALM}/account")
    print()
    print("Next steps:")
    print("  1. Run ./create-user.py to create users")
    print("  2. Create clients in the Keycloak Admin Console")
    print()


if __name__ == "__main__":
    main()
