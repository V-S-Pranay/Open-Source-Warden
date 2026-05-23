"""Agentic loop powered by NVIDIA Nemotron-3-Super via NVIDIA NIM API."""

import json
import logging
import time
from typing import Any

from openai import AsyncOpenAI

from app.agent.safety import is_safe_action
from app.agent.tools import TOOL_DEFINITIONS, execute_tool
from app.config import settings

logger = logging.getLogger(__name__)

_client = AsyncOpenAI(
    base_url=settings.NVIDIA_BASE_URL,
    api_key=settings.NVIDIA_API_KEY,
)


async def run_agent(
    system_prompt: str,
    user_message: str,
    context: dict[str, Any],
    max_iterations: int = 10,
) -> str:
    """
    Agentic loop: Nemotron-3-Super reasons, calls tools, reasons again,
    until it has enough information to produce a final response.

    Returns the model's final text response.
    """
    repo = context.get("repo_full_name", "unknown")
    feature = context.get("feature", "core")
    start = time.monotonic()
    tool_call_count = 0

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    for iteration in range(max_iterations):
        response = await _client.chat.completions.create(
            model=settings.NVIDIA_MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            temperature=0.2,
            max_tokens=2048,
        )

        if not response.choices:
            logger.error("NIM API returned empty choices", extra={"feature": feature, "repo": repo})
            return "I was unable to complete the analysis (empty model response).\n\n---\n*Powered by NVIDIA Nemotron-3-Super via Open-Source-Warden*"

        message = response.choices[0].message

        if not message.tool_calls:
            elapsed = time.monotonic() - start
            logger.info(
                "Agent finished in %.2fs after %d tool calls",
                elapsed,
                tool_call_count,
                extra={"feature": feature, "repo": repo},
            )
            return message.content or ""

        messages.append(message)

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            try:
                tool_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                tool_args = {}

            if not is_safe_action(tool_name, tool_args):
                tool_result = "Action blocked by safety guardrails. Read-only operations only."
                logger.warning(
                    "Blocked unsafe tool call: %s", tool_name,
                    extra={"feature": feature, "repo": repo},
                )
            else:
                try:
                    tool_result = await execute_tool(tool_name, tool_args, context)
                    tool_call_count += 1
                except Exception as exc:
                    tool_result = f"Tool '{tool_name}' encountered an error: {exc}"
                    logger.warning(
                        "Tool %s raised unexpected error: %s", tool_name, exc,
                        extra={"feature": feature, "repo": repo},
                    )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result),
            })

    return (
        "I was unable to complete the analysis within the allowed steps. "
        "Please try again.\n\n"
        "---\n*Powered by NVIDIA Nemotron-3-Super via Open-Source-Warden*"
    )
