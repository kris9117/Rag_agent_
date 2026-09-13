from app.services.database import SessionLocal
from app.services.ticket_service import TicketService
from app.tools.schemas import CreateTicketInput , TicketIdInput


def get_ticket(ticket_id: str) -> dict:
    """Retrieve an IT support ticket."""

    try:
        validated = TicketIdInput(ticket_id=ticket_id)
    except ValueError as exc:
        return {
            "found": False,
            "error": "INVALID_TOOL_INPUT",
            "details": str(exc),
        }

    db = SessionLocal()

    try:
        service = TicketService(db)
        return service.get_ticket(validated.ticket_id)
    finally:
        db.close()


def create_ticket(
    user_id: str,
    category: str,
    description: str,
    priority: str = "medium",
) -> dict:
    """
    Create an IT support ticket after validating the input.
    """

    try:
        validated = CreateTicketInput(
            user_id=user_id,
            category=category,
            description=description,
            priority=priority,
        )
    except ValueError as exc:
        return {
            "created": False,
            "error": "INVALID_TOOL_INPUT",
            "details": str(exc),
        }

    db = SessionLocal()

    try:
        service = TicketService(db)

        return service.create_ticket(
            user_id=validated.user_id,
            category=validated.category,
            description=validated.description,
            priority=validated.priority,
        )

    finally:
        db.close()