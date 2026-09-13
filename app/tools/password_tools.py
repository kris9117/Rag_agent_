from app.services.database import SessionLocal
from app.services.password_service import PasswordService


def check_password_reset_eligibility(user_id: str) -> dict:
    """
    Check whether an employee is eligible for a password reset.

    Args:
        user_id: Enterprise employee ID.

    Returns:
        Structured eligibility result.
    """

    db = SessionLocal()

    try:
        service = PasswordService(db)

        return service.check_password_reset_eligibility(
            user_id
        )

    finally:
        db.close()