import re


def _is_explicit_escalation(query: str) -> bool:
    """
    Return True only for explicit escalation or unresolved-after-troubleshooting
    language.

    Normal phrases such as "VPN keeps failing" must not automatically escalate.
    """

    normalized_query = query.lower().strip()

    explicit_escalation_patterns = [
        "escalate this",
        "escalate the issue",
        "escalate my issue",
        "request escalation",
        "contact a supervisor",
        "contact level 2",
        "contact tier 2",
        "raise this to it support",
        "send this to it support",
    ]

    unresolved_after_troubleshooting_patterns = [
        "still failing after troubleshooting",
        "still not working after troubleshooting",
        "continues to fail after troubleshooting",
        "unable to resolve after troubleshooting",
        "not resolved after troubleshooting",
        "failing repeatedly after troubleshooting",
    ]

    return (
        any(
            pattern in normalized_query
            for pattern in explicit_escalation_patterns
        )
        or any(
            pattern in normalized_query
            for pattern in unresolved_after_troubleshooting_patterns
        )
    )


def _is_explicit_ticket_request(query: str) -> bool:
    """
    Detect explicit ticket creation requests.

    Examples:
    - create a ticket
    - create a high priority software ticket
    - raise a ticket
    - open an incident ticket
    - submit a support ticket
    """

    normalized_query = query.lower().strip()

    return bool(
        re.search(
            r"\b(create|raise|open|log|submit)\b.{0,80}\bticket\b",
            normalized_query,
        )
    )


def determine_route(
    intent: str | None,
    query: str = "",
) -> str:
    """
    Determine the next graph route.

    Possible routes:
    - KNOWLEDGE
    - TOOL
    - RAG_TOOL
    - ACTION
    - ESCALATION
    - CLARIFICATION
    """

    normalized_intent = (intent or "").strip().upper()

    # Explicit escalation always has the highest priority.
    if _is_explicit_escalation(query):
        return "ESCALATION"

    # Explicit ticket request should always become an action.
    # This protects against an LLM classification error.
    if _is_explicit_ticket_request(query):
        return "ACTION"

    route_map = {
        "KNOWLEDGE": "KNOWLEDGE",
        "ACCOUNT_STATUS": "TOOL",
        "DEVICE_STATUS": "TOOL",
        "TICKET_LOOKUP": "TOOL",
        "PASSWORD_RESET": "RAG_TOOL",
        "VPN_TROUBLESHOOTING": "RAG_TOOL",
        "CREATE_TICKET": "ACTION",
        "ESCALATION": "ESCALATION",
        "CLARIFICATION": "CLARIFICATION",
    }

    return route_map.get(normalized_intent, "CLARIFICATION")