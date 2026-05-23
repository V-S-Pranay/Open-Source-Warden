"""Tests for the issue triage feature."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.features import triage


@pytest.mark.asyncio
async def test_triage_run_returns_string(issue_opened_payload: dict):
    mock_result = (
        "## 🤖 Open-Source-Warden Triage\n\n**Category:** Bug Report\n\n"
        "---\n*Powered by NVIDIA Nemotron-3-Super via Open-Source-Warden*"
    )

    with (
        patch("app.features.triage.GitHubClient") as MockClient,
        patch("app.features.triage.run_agent", new_callable=AsyncMock) as mock_agent,
    ):
        mock_client = MagicMock()
        mock_client.get_repo_labels.return_value = ["bug", "enhancement", "good-first-issue"]
        MockClient.return_value = mock_client
        mock_agent.return_value = mock_result

        result = await triage.run(issue_opened_payload)

    assert isinstance(result, str)
    assert "Open-Source-Warden Triage" in result


@pytest.mark.asyncio
async def test_triage_passes_labels_to_agent(issue_opened_payload: dict):
    with (
        patch("app.features.triage.GitHubClient") as MockClient,
        patch("app.features.triage.run_agent", new_callable=AsyncMock) as mock_agent,
    ):
        mock_client = MagicMock()
        mock_client.get_repo_labels.return_value = ["bug", "feature"]
        MockClient.return_value = mock_client
        mock_agent.return_value = "triage result"

        await triage.run(issue_opened_payload)

        call_args = mock_agent.call_args
        user_message: str = call_args[0][1]
        assert "bug" in user_message
        assert "feature" in user_message


def test_is_good_first_issue_positive():
    assert triage.is_good_first_issue("Suggested Labels: `good-first-issue`") is True


def test_is_good_first_issue_negative():
    assert triage.is_good_first_issue("Suggested Labels: `bug`") is False


def test_triage_categorizes_bug():
    result = "**Category:** Bug Report"
    assert "Bug Report" in result


def test_triage_categorizes_feature():
    result = "**Category:** Feature Request"
    assert "Feature Request" in result
