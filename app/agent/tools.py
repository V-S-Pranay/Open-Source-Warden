"""Tool definitions and execution for the Nemotron-3-Super agentic loop."""

import json
import logging
from typing import Any

from app.github.client import GitHubClient

logger = logging.getLogger(__name__)

TOOL_DEFINITIONS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a specific file in the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path relative to repo root"},
                    "repo_full_name": {"type": "string", "description": "owner/repo format"},
                },
                "required": ["path", "repo_full_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories at a given path in the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path, empty string for repo root",
                    },
                    "repo_full_name": {"type": "string"},
                },
                "required": ["path", "repo_full_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_code",
            "description": "Search for a string or function name across all files in the repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term"},
                    "repo_full_name": {"type": "string"},
                },
                "required": ["query", "repo_full_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_issues",
            "description": "Fetch recent closed issues to understand patterns in this repo",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_full_name": {"type": "string"},
                    "count": {"type": "integer", "default": 10},
                },
                "required": ["repo_full_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_readme",
            "description": "Fetch the README of the repository for context about the project",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_full_name": {"type": "string"},
                },
                "required": ["repo_full_name"],
            },
        },
    },
]


async def execute_tool(
    tool_name: str, tool_args: dict[str, Any], context: dict[str, Any]
) -> str:
    """Dispatch a tool call to the appropriate GitHub client method."""
    client: GitHubClient = context["github_client"]
    # Always use the authoritative repo name from context — the LLM can hallucinate/truncate it
    repo = context.get("repo_full_name") or tool_args.get("repo_full_name", "")

    match tool_name:
        case "read_file":
            return client.read_file(repo, tool_args["path"])
        case "list_files":
            results = client.list_files(repo, tool_args.get("path", ""))
            return json.dumps(results)
        case "search_code":
            results = client.search_code(repo, tool_args["query"])
            return json.dumps(results)
        case "get_recent_issues":
            results = client.get_recent_issues(repo, tool_args.get("count", 10))
            return json.dumps(results)
        case "get_readme":
            return client.get_readme(repo)
        case _:
            logger.warning("Unknown tool requested: %s", tool_name)
            return f"Unknown tool: {tool_name}"
