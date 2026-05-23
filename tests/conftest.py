# conftest.py — Shared test fixtures for the Open-Source-Warden test suite.
#
# pytest automatically loads this file before running any test. You never
# import it manually. Every function decorated with @pytest.fixture() becomes
# available to any test in this directory just by listing its name as a
# function argument — pytest finds the match and injects the value for you.
#
# This file defines three fake GitHub webhook payloads (issue opened, PR
# opened, comment posted) that tests use instead of making real GitHub API
# calls. The content is realistic but entirely made up — it just needs the
# right keys so the application code doesn't crash when it reads them.

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
            "number": 1,
            "title": "Bot does not post triage comment after issue is opened",
            "body": (
                "I installed Open-Source-Warden on my repo and opened a new issue, "
                "but no triage comment appeared. The webhook shows 200 OK in the "
                "GitHub delivery log but there is no bot comment on the issue."
            ),
            "user": {"login": "contributor", "id": 1},
            "labels": [],
        },
        "repository": {
            "id": 1,
            "full_name": "V-S-Pranay/Open-Source-Warden",
            "default_branch": "main",
        },
        "installation": {"id": 999},
    }


@pytest.fixture()
def pr_opened_payload() -> dict:
    """Minimal GitHub pull_request.opened webhook payload."""
    return {
        "action": "opened",
        "pull_request": {
            "number": 12,
            "title": "Fix triage comment not posting on reopened issues",
            "body": (
                "The webhook handler only fires on action=opened. "
                "This PR adds handling for action=reopened so the bot "
                "re-triages issues that are closed and reopened."
            ),
            "user": {"login": "contributor", "id": 2},
        },
        "repository": {
            "id": 1,
            "full_name": "V-S-Pranay/Open-Source-Warden",
            "default_branch": "main",
        },
        "installation": {"id": 999},
    }


@pytest.fixture()
def comment_payload() -> dict:
    """Minimal GitHub issue_comment.created webhook payload."""
    return {
        "action": "created",
        "issue": {
            "number": 1,
            "title": "Bot does not post triage comment after issue is opened",
            "body": (
                "I installed Open-Source-Warden on my repo and opened a new issue, "
                "but no triage comment appeared."
            ),
            "user": {"login": "contributor", "id": 1},
            "labels": [],
            "html_url": "https://github.com/V-S-Pranay/Open-Source-Warden/issues/1",
        },
        "comment": {"id": 100, "body": "/copilot help", "user": {"login": "contributor"}},
        "repository": {
            "id": 1,
            "full_name": "V-S-Pranay/Open-Source-Warden",
            "default_branch": "main",
        },
        "installation": {"id": 999},
    }
