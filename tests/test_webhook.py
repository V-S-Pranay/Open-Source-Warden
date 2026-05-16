"""Tests for webhook signature verification and event routing."""

import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from app.config import settings
from app.security import verify_signature


def _sign(payload: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return f"sha256={sig}"


def test_verify_signature_valid():
    payload = b'{"action": "opened"}'
    secret = "test-secret"
    sig = _sign(payload, secret)

    original = settings.GITHUB_WEBHOOK_SECRET
    settings.GITHUB_WEBHOOK_SECRET = secret
    assert verify_signature(payload, sig) is True
    settings.GITHUB_WEBHOOK_SECRET = original


def test_verify_signature_invalid():
    payload = b'{"action": "opened"}'
    assert verify_signature(payload, "sha256=badhash") is False


def test_verify_signature_missing_header():
    assert verify_signature(b"payload", "") is False


def test_verify_signature_wrong_prefix():
    assert verify_signature(b"payload", "md5=abc123") is False


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model" in data


def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "MaintainerCopilot"


def test_webhook_rejects_unsigned_request(client: TestClient, issue_opened_payload: dict):
    response = client.post(
        "/webhook",
        content=json.dumps(issue_opened_payload),
        headers={"X-GitHub-Event": "issues", "Content-Type": "application/json"},
    )
    assert response.status_code == 401
