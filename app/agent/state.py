from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    """State carried through the IT support agent workflow."""

    request_id: str
    user_id: str | None
    query: str

    intent: str | None
    entities: dict[str, Any]
    route: str | None

    retrieved_context: list[dict[str, Any]]

    tool_calls: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]

    validation_errors: list[str]

    retry_count: int

    response: str | None
    status: str | None

    escalation_required: bool