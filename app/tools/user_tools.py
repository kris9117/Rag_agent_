from app.services.database import SessionLocal
from app.services.user_service import UserService
from app.tools.schemas import UserIdInput


def get_user_profile(user_id: str) -> dict:
    """Retrieve an employee profile."""

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
        service = UserService(db)
        return service.get_user_profile(validated.user_id)
    finally:
        db.close()