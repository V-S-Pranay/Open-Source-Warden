"""Feature 1: Automatic issue triage."""

import logging

from app.agent.core import run_agent
from app.agent.prompts import TRIAGE_PROMPT
from app.github.client import GitHubClient

logger = logging.getLogger(__name__)


async def run(data: dict) -> str:
    """
    Triage a newly opened issue and return a formatted markdown comment.

    Reads the repo's labels, README, and relevant source files before
    producing a structured triage report grounded in the actual codebase.
    """
    repo_full_name: str = data["repository"]["full_name"]
    installation_id: int = data["installation"]["id"]
    issue = data["issue"]

    client = GitHubClient(installation_id)
    labels = client.get_repo_labels(repo_full_name)

    user_message = (
        f"Repository: {repo_full_name}\n"
        f"Issue #{issue['number']}: {issue['title']}\n\n"
        f"Issue body:\n{issue.get('body') or '(no description provided)'}\n\n"
        f"Existing repo labels: {', '.join(labels) if labels else 'none defined'}\n\n"
        "Please triage this issue."
    )

    context = {
        "github_client": client,
        "repo_full_name": repo_full_name,
        "feature": "triage",
    }

    result = await run_agent(TRIAGE_PROMPT, user_message, context)
    logger.info(
        "Triage complete for issue #%d", issue["number"],
        extra={"feature": "triage", "repo": repo_full_name},
    )
    return result


def is_good_first_issue(triage_result: str) -> bool:
    """Return True if the triage output suggests a good-first-issue label."""
    lower = triage_result.lower()
    return "good-first-issue" in lower or "good first issue" in lower
