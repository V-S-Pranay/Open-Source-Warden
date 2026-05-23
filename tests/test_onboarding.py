"""Tests for the newcomer onboarding feature."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.features import onboarding


@pytest.mark.asyncio
async def test_onboarding_run_returns_string(issue_opened_payload: dict):
    mock_result = (
        "## 👋 Good First Issue — Contributor Guide\n\n"
        "Hey there, future contributor!\n\n"
        "---\n*Powered by NVIDIA Nemotron-3-Super via Open-Source-Warden*"
    )

    with (
        patch("app.features.onboarding.GitHubClient") as MockClient,
        patch("app.features.onboarding.run_agent", new_callable=AsyncMock) as mock_agent,
    ):
        MockClient.return_value = MagicMock()
        mock_agent.return_value = mock_result

        result = await onboarding.run(issue_opened_payload)

    assert isinstance(result, str)
    assert "Contributor Guide" in result


@pytest.mark.asyncio
async def test_onboarding_links_to_files(issue_opened_payload: dict):
    mock_result = (
        "## 👋 Good First Issue — Contributor Guide\n\n"
        "**Where to start:**\n- The relevant code lives in `src/upload.py`\n"
    )

    with (
        patch("app.features.onboarding.GitHubClient") as MockClient,
        patch("app.features.onboarding.run_agent", new_callable=AsyncMock) as mock_agent,
    ):
        MockClient.return_value = MagicMock()
        mock_agent.return_value = mock_result

        result = await onboarding.run(issue_opened_payload)

    assert "`src/upload.py`" in result
