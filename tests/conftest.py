"""Shared pytest fixtures for MaintainerCopilot tests."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Return a synchronous test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture()
def issue_opened_payload() -> dict:
    """Minimal GitHub issues.opened webhook payload."""
    return {
        "action": "opened",
        "issue": {
            "number": 42,
            "title": "App crashes when uploading large files",
            "body": "When I upload a file larger than 10MB the app crashes with a 500 error.",
            "user": {"login": "reporter", "id": 1},
            "labels": [],
        },
        "repository": {"id": 1, "full_name": "test-org/test-repo", "default_branch": "main"},
        "installation": {"id": 999},
    }


@pytest.fixture()
def pr_opened_payload() -> dict:
    """Minimal GitHub pull_request.opened webhook payload."""
    return {
        "action": "opened",
        "pull_request": {
            "number": 7,
            "title": "Fix file upload size validation",
            "body": "Adds a 10MB cap and returns a 413 instead of crashing.",
            "user": {"login": "contributor", "id": 2},
        },
        "repository": {"id": 1, "full_name": "test-org/test-repo", "default_branch": "main"},
        "installation": {"id": 999},
    }


@pytest.fixture()
def comment_payload() -> dict:
    """Minimal GitHub issue_comment.created webhook payload."""
    return {
        "action": "created",
        "issue": {
            "number": 42,
            "title": "App crashes when uploading large files",
            "body": "When I upload a file larger than 10MB the app crashes.",
            "user": {"login": "reporter", "id": 1},
            "labels": [],
            "html_url": "https://github.com/test-org/test-repo/issues/42",
        },
        "comment": {"id": 100, "body": "/copilot help", "user": {"login": "reporter"}},
        "repository": {"id": 1, "full_name": "test-org/test-repo", "default_branch": "main"},
        "installation": {"id": 999},
    }
