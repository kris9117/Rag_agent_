from sqlalchemy.orm import Session

from app.models.database_models import Account


class AccountService:
    """Business logic for employee account operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_account_status(self, user_id: str) -> dict:
        """Return the current account status for an employee."""

        account = (
            self.db.query(Account)
            .filter(Account.user_id == user_id)
            .first()
        )

        if account is None:
            return {
                "found": False,
                "user_id": user_id,
                "error": "ACCOUNT_NOT_FOUND",
            }

        return {
            "found": True,
            "user_id": account.user_id,
            "status": account.status,
            "locked": account.locked,
            "mfa_enabled": account.mfa_enabled,
            "failed_attempts": account.failed_attempts,
            "password_last_changed": (
                account.password_last_changed.isoformat()
            ),
        }