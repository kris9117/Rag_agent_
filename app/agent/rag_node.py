from app.agent.state import AgentState
from app.rag.rag_service import RAGService
from app.services.llm_service import LLMService


def response_requires_escalation(
    query: str,
    response: str,
) -> bool:
    """Detect whether the request requires escalation."""

    query_lower = " ".join(query.lower().split())
    response_lower = " ".join(response.lower().split())

    explicit_user_terms = [
        "escalate",
        "escalation",
        "contact support",
        "contact a supervisor",
        "contact level 2",
        "contact tier 2",
        "raise this to it support",
        "send this to it support",
        "speak to a supervisor",
        "talk to a supervisor",
        "still failing after troubleshooting",
        "still not working after troubleshooting",
        "continues to fail after troubleshooting",
        "unable to resolve after troubleshooting",
        "not resolved after troubleshooting",
        "does not work after troubleshooting",
        "issue is still failing",
        "issue still fails",
        "failing repeatedly",
        "keeps failing repeatedly",
    ]

    security_terms = [
        "suspicious activity",
        "suspicious email",
        "phishing",
        "asked for my password",
        "asking for my password",
        "account compromise",
        "unauthorized access",
        "security incident",
        "stolen credentials",
        "credential theft",
    ]

    critical_response_terms = [
        "security incident",
        "account compromise",
        "requires immediate escalation",
        "security team",
    ]

    user_requested_escalation = any(
        term in query_lower
        for term in explicit_user_terms
    )

    security_issue = any(
        term in query_lower
        for term in security_terms
    )

    critical_response_issue = any(
        term in response_lower
        for term in critical_response_terms
    )

    # Password reset is a normal knowledge-base request unless the
    # user explicitly reports compromise, phishing, or unauthorized access.
    password_reset_query = (
        "password" in query_lower
        and any(
            term in query_lower
            for term in [
                "reset",
                "forgot",
                "change",
                "unlock",
            ]
        )
    )

    if password_reset_query and not security_issue:
        return user_requested_escalation

    return (
        user_requested_escalation
        or security_issue
        or critical_response_issue
    )


def rag_node(state: AgentState) -> AgentState:
    """Retrieve KB evidence and generate a grounded response."""

    query = state.get("query", "").strip()

    if not query:
        return {
            **state,
            "retrieved_context": [],
            "validation_errors": [
                "The query cannot be empty."
            ],
            "response": (
                "I need a valid question to search the knowledge base."
            ),
            "status": "RAG_FAILED",
        }

    try:
        rag_service = RAGService()
        llm_service = LLMService()

        retrieved_context = rag_service.retrieve(
            query=query,
            candidate_k=10,
            top_k=5,
        )

        response = llm_service.generate_rag_response(
            query=query,
            context=retrieved_context,
        )

        return {
            **state,
            "retrieved_context": retrieved_context,
            "response": response,
            "status": "RAG_COMPLETED",
            "validation_errors": [],
            "escalation_required": response_requires_escalation(
                query=query, response=response
            ),
        }

    except Exception as exc:
        import logging

        logging.exception("RAG execution failed")

        return {
            **state,
            "retrieved_context": [],
            "validation_errors": [
                f"RAG execution failed: {type(exc).__name__}: {exc}"
            ],
            "response": (
                "I could not complete the knowledge-base search. "
                "Please contact IT support."
            ),
            "status": "RAG_FAILED",
            "escalation_required": True,
        }