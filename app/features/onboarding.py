"""Feature 3: Newcomer onboarding guide for good-first-issues."""

import logging

from app.agent.core import run_agent
from app.agent.prompts import ONBOARDING_PROMPT
from app.github.client import GitHubClient

logger = logging.getLogger(__name__)


async def run(data: dict) -> str:
    """
    Generate a welcoming contributor guide for a good-first-issue.

    Reads the README and relevant source files to provide accurate,
    project-specific onboarding instructions.
    """
    repo_full_name: str = data["repository"]["full_name"]
    installation_id: int = data["installation"]["id"]
    issue = data["issue"]

    client = GitHubClient(installation_id)

    user_message = (
        f"Repository: {repo_full_name}\n"
        f"Issue #{issue['number']}: {issue['title']}\n\n"
        f"Issue body:\n{issue.get('body') or '(no description provided)'}\n\n"
        "Please generate a newcomer contributor guide for this good-first-issue."
    )

    context = {
        "github_client": client,
        "repo_full_name": repo_full_name,
        "feature": "onboarding",
    }

    result = await run_agent(ONBOARDING_PROMPT, user_message, context)
    logger.info(
        "Onboarding guide generated for issue #%d", issue["number"],
        extra={"feature": "onboarding", "repo": repo_full_name},
    )
    return result
