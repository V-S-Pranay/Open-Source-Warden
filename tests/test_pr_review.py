"""Tests for the PR review assistant feature."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.features import pr_review


@pytest.mark.asyncio
async def test_pr_review_run_returns_string(pr_opened_payload: dict):
    mock_result = (
        "## 🔍 MaintainerCopilot PR Review\n\n"
        "**Summary of changes:** This PR fixes the file upload size validation.\n\n"
        "---\n*Powered by NVIDIA Nemotron-3-Super via MaintainerCopilot*"
    )

    with (
        patch("app.features.pr_review.GitHubClient") as MockClient,
        patch("app.features.pr_review.run_agent", new_callable=AsyncMock) as mock_agent,
    ):
        mock_client = MagicMock()
        mock_client.get_pull_request_files.return_value = [
            {"filename": "src/upload.py", "status": "modified", "patch": "@@ -10,6 +10,10 @@"}
        ]
        MockClient.return_value = mock_client
        mock_agent.return_value = mock_result

        result = await pr_review.run(pr_opened_payload)

    assert isinstance(result, str)
    assert "PR Review" in result


@pytest.mark.asyncio
async def test_pr_review_includes_changed_files(pr_opened_payload: dict):
    with (
        patch("app.features.pr_review.GitHubClient") as MockClient,
        patch("app.features.pr_review.run_agent", new_callable=AsyncMock) as mock_agent,
    ):
        mock_client = MagicMock()
        mock_client.get_pull_request_files.return_value = [
            {"filename": "app/upload.py", "status": "modified", "patch": "some diff"}
        ]
        MockClient.return_value = mock_client
        mock_agent.return_value = "review result"

        await pr_review.run(pr_opened_payload)

        user_message: str = mock_agent.call_args[0][1]
        assert "app/upload.py" in user_message
