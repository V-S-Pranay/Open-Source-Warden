"""Tests for the reproduction steps feature."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.features import reproduction


@pytest.mark.asyncio
async def test_reproduction_run_returns_string(issue_opened_payload: dict):
    mock_result = (
        "## 🔬 Reproduction Steps\n\n**Steps to reproduce:**\n1. Step one\n\n"
        "---\n*Powered by NVIDIA Nemotron-3-Super via Open-Source-Warden*"
    )

    with (
        patch("app.features.reproduction.GitHubClient") as MockClient,
        patch("app.features.reproduction.run_agent", new_callable=AsyncMock) as mock_agent,
    ):
        MockClient.return_value = MagicMock()
        mock_agent.return_value = mock_result

        result = await reproduction.run(issue_opened_payload)

    assert isinstance(result, str)
    assert "Reproduction Steps" in result


@pytest.mark.asyncio
async def test_reproduction_includes_issue_title(issue_opened_payload: dict):
    with (
        patch("app.features.reproduction.GitHubClient") as MockClient,
        patch("app.features.reproduction.run_agent", new_callable=AsyncMock) as mock_agent,
    ):
        MockClient.return_value = MagicMock()
        mock_agent.return_value = "repro result"

        await reproduction.run(issue_opened_payload)

        call_args = mock_agent.call_args
        user_message: str = call_args[0][1]
        assert "crashes when uploading large files" in user_message


@pytest.mark.asyncio
async def test_reproduction_uses_correct_prompt(issue_opened_payload: dict):
    with (
        patch("app.features.reproduction.GitHubClient") as MockClient,
        patch("app.features.reproduction.run_agent", new_callable=AsyncMock) as mock_agent,
    ):
        MockClient.return_value = MagicMock()
        mock_agent.return_value = "repro result"

        await reproduction.run(issue_opened_payload)

        system_prompt: str = mock_agent.call_args[0][0]
        assert "reproduction" in system_prompt.lower() or "REPRODUCTION" in system_prompt
