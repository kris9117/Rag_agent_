import logging
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.agent.graph import agent_graph
from app.api.schemas import SupportRequest, SupportResponse
from app.services.observability import Timer, log_event


router = APIRouter(
    prefix="/api/v1",
    tags=["support"],
)


@router.post(
    "/support",
    response_model=SupportResponse,
)
def support_request(request: SupportRequest) -> SupportResponse:
    """Process an employee IT support request."""

    request_id = f"REQ-{uuid4().hex[:12].upper()}"

    timer = Timer()

    log_event(
    "support_request_started",
    request_id=request_id,
    user_id=request.user_id,
    query_length=len(request.query),
    )

    initial_state = {
        "request_id": request_id,
        "user_id": request.user_id,
        "query": request.query,
        "intent": None,
        "entities": {},
        "route": None,
        "retrieved_context": [],
        "tool_calls": [],
        "tool_results": [],
        "validation_errors": [],
        "retry_count": 0,
        "response": None,
        "status": None,
        "escalation_required": False,
    }

    try:
        result = agent_graph.invoke(initial_state)

        log_event(
            "support_request_completed",
            request_id=request_id,
            user_id=result.get("user_id"),
            intent=result.get("intent"),
            route=result.get("route"),
            status=result.get("status"),
            escalation_required=result.get(
                "escalation_required",
                False,
            ),
            tool_call_count=len(
                result.get("tool_calls", [])
            ),
            retrieval_count=len(
                result.get("retrieved_context", [])
            ),
            latency_ms=timer.elapsed_ms(),
        )

        return SupportResponse(
            request_id=request_id,
            user_id=request.user_id,
            intent=result.get("intent"),
            route=result.get("route"),
            status=result.get("status"),
            response=result.get("response"),
            escalation_required=result.get(
                "escalation_required",
                False,
            ),
        )

    except Exception as exc:
        logger = logging.getLogger(__name__)

        logger.exception(
            "Support request failed | request_id=%s | user_id=%s",
            request_id,
            request.user_id,
        )

        log_event(
            "support_request_failed",
            request_id=request_id,
            user_id=request.user_id,
            error_type=type(exc).__name__,
            latency_ms=timer.elapsed_ms(),
        )

        raise HTTPException(
            status_code=500,
            detail={
                "request_id": request_id,
                "error": "SUPPORT_REQUEST_FAILED",
                "message": (
                    "Unable to process the support request "
                    "at this time."
                ),
            },
        ) from exc