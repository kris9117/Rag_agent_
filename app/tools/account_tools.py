from app.services.account_service import AccountService
from app.services.database import SessionLocal
from app.tools.schemas import UserIdInput


def get_account_status(user_id: str) -> dict:
    """Retrieve account status for an employee."""

    try:
        validated = UserIdInput(user_id=user_id)
    except ValueError as exc:
        return {
            "found": False,
            "error": "INVALID_TOOL_INPUT",
            "details": str(exc),
        }

    db = SessionLocal()

    try:
        service = AccountService(db)
        return service.get_account_status(validated.user_id)
    finally:
        db.close()