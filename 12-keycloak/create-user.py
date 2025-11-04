#!/usr/bin/env python3
"""
Keycloak User Creation Script
Automates user creation via Keycloak Admin REST API
"""

import requests
import sys

# Configuration - CHANGE THESE VALUES
KEYCLOAK_URL = "https://keycloak.ltu-m7011e-johan.se"
REALM = "myapp"
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin-change-this-password"

# User details
USERNAME = "testuser"
EMAIL = "test@example.com"
FIRST_NAME = "Test"
LAST_NAME = "User"
PASSWORD = "testpass123"


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
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("✅ Admin token obtained\n")
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get admin token: {e}")
        print("Check your credentials and Keycloak URL.")
        sys.exit(1)


def create_user(token, username, email, first_name, last_name, password):
    """Create a new user in Keycloak"""
    print(f"Step 2: Creating user '{username}'...")

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

    try:
        response = requests.post(url, json=user_data, headers=headers)

        if response.status_code == 201:
            # Get user ID from Location header
            user_id = response.headers["Location"].split("/")[-1]
            print(f"✅ User created with ID: {user_id}\n")

            # Set password
            print("Step 3: Setting password...")
            password_data = {
                "type": "password",
                "value": password,
                "temporary": False
            }
            pwd_url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users/{user_id}/reset-password"
            pwd_response = requests.put(pwd_url, json=password_data, headers=headers)

            if pwd_response.status_code == 204:
                print("✅ Password set successfully\n")
                return user_id
            else:
                print(f"❌ Failed to set password: {pwd_response.text}")
                sys.exit(1)

        elif response.status_code == 409:
            print(f"⚠️  User '{username}' already exists")
            sys.exit(0)
        else:
            print(f"❌ Failed to create user: {response.text}")
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)


def main():
    print("=" * 40)
    print("Keycloak User Creation Script")
    print("=" * 40)
    print()

    # Get admin token
    token = get_admin_token()

    # Create user
    create_user(
        token=token,
        username=USERNAME,
        email=EMAIL,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        password=PASSWORD
    )

    print("=" * 40)
    print("✅ User created successfully!")
    print("=" * 40)
    print()
    print("Login credentials:")
    print(f"  Username: {USERNAME}")
    print(f"  Password: {PASSWORD}")
    print()
    print("Test login at:")
    print(f"  {KEYCLOAK_URL}/realms/{REALM}/account")
    print()


if __name__ == "__main__":
    main()
