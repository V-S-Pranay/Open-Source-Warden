"""Webhook signature verification to ensure payloads come from GitHub."""

import hashlib
import hmac

from app.config import settings


def verify_signature(payload: bytes, signature_header: str) -> bool:
    """Verify that the webhook payload came from GitHub using HMAC-SHA256."""
    if not signature_header or not signature_header.startswith("sha256="):
        return False

    expected = hmac.new(
        settings.GITHUB_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    received = signature_header.removeprefix("sha256=")
    return hmac.compare_digest(expected, received)
