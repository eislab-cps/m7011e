"""Exercise all three teaching examples without a live Keycloak server."""

import importlib.util
import json
import time
from pathlib import Path
from unittest.mock import Mock

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

EXAMPLES = [
    "example-part-1-todo-basic",
    "example-part-2-todo-secure",
    "example-part-3-todo-rbac",
]


@pytest.fixture(params=EXAMPLES)
def api(request, monkeypatch):
    path = Path(__file__).parents[1] / request.param / "backend/app.py"
    spec = importlib.util.spec_from_file_location("keycloak_todo_example", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.app.config["TESTING"] = True
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(private_key.public_key()))
    jwk["kid"] = "test-key"
    module.public_keys_cache = {"keys": [jwk]}
    module.public_keys_fetched_at = time.monotonic()
    # An accidental JWKS request should fail locally rather than contacting a realm.
    if hasattr(module, "requests"):
        monkeypatch.setattr(
            module.requests,
            "get",
            Mock(side_effect=AssertionError("Unexpected network request")),
        )
    return module, private_key, jwk, request.param


@pytest.fixture
def secure_api(api):
    if api[3] == EXAMPLES[0]:
        pytest.skip("Example 1 deliberately does not verify tokens")
    return api


def token_for(api, **claims):
    module, private_key, _, _ = api
    payload = {
        "iss": getattr(module, "KEYCLOAK_ISSUER", "https://example.test/realms/myapp"),
        "aud": getattr(module, "API_AUDIENCE", "todo-api"),
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
    "header", [None, "Basic abc", "Bearer", "Bearer a b", "Bearer invalid"]
)
def test_requires_bearer_token(api, header):
    headers = {} if header is None else {"Authorization": header}
    assert (
        api[0].app.test_client().get("/api/todos", headers=headers).status_code == 401
    )


@pytest.mark.parametrize(
    "claims",
    [
        {"aud": "account"},
        {"iss": "https://another-issuer.example/realms/myapp"},
        {"exp": int(time.time()) - 60},
        {"sub": None},
        {"sub": ""},
    ],
)
def test_rejects_wrong_claims(secure_api, claims):
    api = secure_api
    assert (
        api[0]
        .app.test_client()
        .get("/api/todos", headers=headers_for(api, **claims))
        .status_code
        == 401
    )


@pytest.mark.parametrize("missing", ["exp", "iss", "sub", "aud"])
def test_requires_claims(secure_api, missing):
    api = secure_api
    payload = jwt.decode(token_for(api), options={"verify_signature": False})
    del payload[missing]
    token = jwt.encode(payload, api[1], algorithm="RS256", headers={"kid": "test-key"})
    assert (
        api[0]
        .app.test_client()
        .get("/api/todos", headers={"Authorization": f"Bearer {token}"})
        .status_code
        == 401
    )


@pytest.mark.parametrize("body", [[], None, {"text": 123}, {"text": " "}])
def test_invalid_input_returns_bad_request(api, body):
    response = (
        api[0].app.test_client().post("/api/todos", json=body, headers=headers_for(api))
    )
    assert response.status_code == 400


def test_ownership_crud_and_admin_difference(api):
    client = api[0].app.test_client()
    alice = headers_for(api)
    bob = headers_for(api, sub="bob", preferred_username="bob")
    first = client.post("/api/todos", json={"text": " Alice's todo "}, headers=alice)
    second = client.post("/api/todos", json={"text": "Bob's todo"}, headers=bob)
    assert first.status_code == second.status_code == 201
    assert first.json["text"] == "Alice's todo"
    assert client.get("/api/todos", headers=alice).json == [first.json]
    bob_url = f"/api/todos/{second.json['id']}"
    assert client.delete(bob_url, headers=alice).status_code == 403
    assert client.put(f"{bob_url}/toggle", headers=alice).status_code == 403
    assert (
        client.put(f"/api/todos/{first.json['id']}/toggle", headers=alice).json[
            "completed"
        ]
        is True
    )
    admin = headers_for(api, realm_access={"roles": ["admin"]})
    if api[3] == EXAMPLES[1]:
        # Example 2 intentionally has no admin override.
        assert len(client.get("/api/todos", headers=admin).json) == 1
        assert client.put(f"{bob_url}/toggle", headers=admin).status_code == 403
        assert client.delete(bob_url, headers=admin).status_code == 403
        assert client.delete(bob_url, headers=bob).status_code == 204
    else:
        assert len(client.get("/api/todos", headers=admin).json) == 2
        assert client.put(f"{bob_url}/toggle", headers=admin).json["completed"] is True
        assert client.delete(bob_url, headers=admin).status_code == 204
    assert client.delete(bob_url, headers=bob).status_code == 404


def test_refreshes_keys_on_rotation(secure_api, monkeypatch):
    module, _, jwk, _ = secure_api
    module.public_keys_cache = {"keys": []}
    response = Mock()
    response.json.return_value = {"keys": [jwk]}
    fetch = Mock(return_value=response)
    monkeypatch.setattr(module.requests, "get", fetch)
    assert module.verify_token(token_for(secure_api))["sub"] == "alice"
    fetch.assert_called_once_with(
        module.KEYCLOAK_CERTS_URL, timeout=10, verify=not module.INSECURE
    )
    response.raise_for_status.assert_called_once()


def test_signature_verification_difference(api):
    # This deliberately forged token demonstrates why example 1 is insecure.
    forged = jwt.encode(
        {"sub": "mallory", "exp": 1},
        "untrusted-demo-secret-for-testing-only",
        algorithm="HS256",
    )
    response = (
        api[0]
        .app.test_client()
        .get("/api/todos", headers={"Authorization": f"Bearer {forged}"})
    )
    assert response.status_code == (200 if api[3] == EXAMPLES[0] else 401)


def test_endpoint_errors_are_not_reported_as_authentication_failures(api):
    @api[0].app.route("/test-error")
    @api[0].require_auth
    def failing_endpoint():
        raise RuntimeError("Application error")

    with pytest.raises(RuntimeError, match="Application error"):
        api[0].app.test_client().get("/test-error", headers=headers_for(api))
