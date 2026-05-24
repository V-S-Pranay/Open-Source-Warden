"""GitHub App JWT authentication and installation token management."""

import time

import jwt
from github import Github, GithubIntegration

from app.config import settings


def _load_private_key() -> str:
    if settings.GITHUB_PRIVATE_KEY:
        return settings.GITHUB_PRIVATE_KEY.replace("\\n", "\n")
    with open(settings.GITHUB_PRIVATE_KEY_PATH, "r") as f:
        return f.read()


def generate_app_jwt() -> str:
    """Generate a short-lived JWT signed with the GitHub App private key."""
    private_key = _load_private_key()
    now = int(time.time())
    payload = {
        "iat": now - 60,    # issued 60s in the past to handle clock drift
        "exp": now + 600,   # valid for 10 minutes
        "iss": settings.GITHUB_APP_ID,
    }
    return jwt.encode(payload, private_key, algorithm="RS256")


def get_installation_token(installation_id: int) -> str:
    """Exchange the App JWT for a short-lived installation access token."""
    private_key = _load_private_key()
    integration = GithubIntegration(settings.GITHUB_APP_ID, private_key)
    token = integration.get_access_token(installation_id)
    return token.token


def get_github_client(installation_id: int) -> Github:
    """Return an authenticated PyGithub client scoped to the installation."""
    token = get_installation_token(installation_id)
    return Github(token)
