import time
from typing import Any

from app.tools.registry import TOOL_REGISTRY
from app.services.observability import log_event


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """Execute an approved enterprise tool."""

    started_at = time.perf_counter()

    log_event(
        "tool_execution_started",
        tool_name=tool_name,
        argument_keys=list(arguments.keys()),
    )

    tool = TOOL_REGISTRY.get(tool_name)

    if tool is None:
        elapsed_ms = round(
            (time.perf_counter() - started_at) * 1000,
            2,
        )

        log_event(
            "tool_execution_failed",
            tool_name=tool_name,
            error="UNKNOWN_TOOL",
            elapsed_ms=elapsed_ms,
        )

        return {
            "success": False,
            "error": "UNKNOWN_TOOL",
            "tool_name": tool_name,
        }

    try:
        result = tool(**arguments)

        elapsed_ms = round(
            (time.perf_counter() - started_at) * 1000,
            2,
        )

        log_event(
            "tool_execution_completed",
            tool_name=tool_name,
            success=True,
            elapsed_ms=elapsed_ms,
        )

        return {
            "success": True,
            "tool_name": tool_name,
            "result": result,
        }

    except Exception as exc:
        elapsed_ms = round(
            (time.perf_counter() - started_at) * 1000,
            2,
        )

        log_event(
            "tool_execution_failed",
            tool_name=tool_name,
            error="TOOL_EXECUTION_ERROR",
            elapsed_ms=elapsed_ms,
        )

        return {
            "success": False,
            "error": "TOOL_EXECUTION_ERROR",
            "tool_name": tool_name,
            "details": str(exc),
        }