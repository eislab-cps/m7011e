"""Verify JWT validation and isolation without a live Keycloak server."""

import importlib.util
import json
import time
from pathlib import Path
from unittest.mock import Mock

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa


@pytest.fixture
def api():
    spec = importlib.util.spec_from_file_location(
        "keycloak_todo_example", Path(__file__).with_name("app.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(private_key.public_key()))
    jwk["kid"] = "test-key"
    module.public_keys_cache = {"keys": [jwk]}
    module.public_keys_fetched_at = time.monotonic()
    module.app.config["TESTING"] = True
    return module, private_key, jwk


def token_for(api, **claims):
    module, private_key, _ = api
    payload = {
        "iss": module.KEYCLOAK_ISSUER,
        "aud": module.API_AUDIENCE,
        "sub": "alice",
        "preferred_username": "alice",
        "exp": int(time.time()) + 300,
    }
    payload.update(claims)
    return jwt.encode(
        payload, private_key, algorithm="RS256", headers={"kid": "test-key"}
    )


def headers_for(api, **claims):
    return {"Authorization": f"Bearer {token_for(api, **claims)}"}


@pytest.mark.parametrize(
    "claims",
    [
        {"aud": "account"},
        {"iss": "https://another-issuer.example/realms/myapp"},
        {"exp": int(time.time()) - 60},
        {"sub": None},
    ],
)
def test_rejects_wrong_claims(api, claims):
    response = (
        api[0].app.test_client().get("/api/todos", headers=headers_for(api, **claims))
    )
    assert response.status_code == 401


def test_requires_expiration(api):
    module, private_key, _ = api
    token = jwt.encode(
        {"iss": module.KEYCLOAK_ISSUER, "aud": module.API_AUDIENCE, "sub": "alice"},
        private_key,
        algorithm="RS256",
        headers={"kid": "test-key"},
    )
    response = module.app.test_client().get(
        "/api/todos", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401


@pytest.mark.parametrize("body", [[], None, {"text": 123}, {"text": " "}])
def test_invalid_input_returns_bad_request(api, body):
    response = (
        api[0].app.test_client().post("/api/todos", json=body, headers=headers_for(api))
    )
    assert response.status_code == 400


def test_users_cannot_access_each_others_todos(api):
    client = api[0].app.test_client()
    alice = headers_for(api)
    bob = headers_for(api, sub="bob", preferred_username="bob")
    first = client.post("/api/todos", json={"text": "Alice's todo"}, headers=alice)
    second = client.post("/api/todos", json={"text": "Bob's todo"}, headers=bob)
    assert first.status_code == second.status_code == 201
    assert client.get("/api/todos", headers=alice).json == [first.json]
    assert (
        client.delete(f"/api/todos/{second.json['id']}", headers=alice).status_code
        == 403
    )
    assert (
        client.put(f"/api/todos/{second.json['id']}/toggle", headers=alice).status_code
        == 403
    )
    admin = headers_for(api, realm_access={"roles": ["admin"]})
    assert len(client.get("/api/todos", headers=admin).json) == 2
    assert (
        client.delete(f"/api/todos/{second.json['id']}", headers=admin).status_code
        == 204
    )


def test_refreshes_keys_on_rotation(api, monkeypatch):
    module, _, jwk = api
    module.public_keys_cache = {"keys": []}
    response = Mock()
    response.json.return_value = {"keys": [jwk]}
    fetch = Mock(return_value=response)
    monkeypatch.setattr(module.requests, "get", fetch)
    assert module.verify_token(token_for(api))["sub"] == "alice"
    fetch.assert_called_once()
