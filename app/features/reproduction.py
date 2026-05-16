"""Feature 2: Reproduction steps generator for bug reports."""

import logging

from app.agent.core import run_agent
from app.agent.prompts import REPRODUCTION_PROMPT
from app.github.client import GitHubClient

logger = logging.getLogger(__name__)


async def run(data: dict) -> str:
    """
    Generate step-by-step reproduction instructions for a bug report.

    The agent MUST read relevant source files before writing any steps —
    every step must reference real code from the repository.
    """
    repo_full_name: str = data["repository"]["full_name"]
    installation_id: int = data["installation"]["id"]
    issue = data["issue"]

    client = GitHubClient(installation_id)

    user_message = (
        f"Repository: {repo_full_name}\n"
        f"Issue #{issue['number']}: {issue['title']}\n\n"
        f"Bug report:\n{issue.get('body') or '(no description provided)'}\n\n"
        "Please generate detailed, codebase-grounded reproduction steps."
    )

    context = {
        "github_client": client,
        "repo_full_name": repo_full_name,
        "feature": "reproduction",
    }

    result = await run_agent(REPRODUCTION_PROMPT, user_message, context)
    logger.info(
        "Reproduction steps generated for issue #%d", issue["number"],
        extra={"feature": "reproduction", "repo": repo_full_name},
    )
    return result
