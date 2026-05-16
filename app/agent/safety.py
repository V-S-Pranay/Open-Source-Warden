"""Safety guardrails — the agent may only read and post comments."""

ALLOWED_READ_TOOLS: frozenset[str] = frozenset({
    "read_file",
    "list_files",
    "search_code",
    "get_recent_issues",
    "get_readme",
})

ALLOWED_WRITE_TOOLS: frozenset[str] = frozenset({
    "post_comment",  # the only permitted write operation
})


def is_safe_action(tool_name: str, tool_args: dict) -> bool:
    """
    Return True only if the action is safe to execute.

    The agent may ONLY read from the repository and post comments.
    It may NEVER: delete issues, close PRs, push code, modify files,
    change settings, or take any irreversible action.
    """
    return tool_name in ALLOWED_READ_TOOLS or tool_name in ALLOWED_WRITE_TOOLS
