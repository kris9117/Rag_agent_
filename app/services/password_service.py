from sqlalchemy.orm import Session

from app.models.database_models import Account


class PasswordService:
    """Business logic for password reset eligibility."""

    MAX_FAILED_ATTEMPTS = 5

    def __init__(self, db: Session):
        self.db = db

    def check_password_reset_eligibility(
        self,
        user_id: str,
    ) -> dict:
        """Determine whether an employee can reset their password."""

        account = (
            self.db.query(Account)
            .filter(Account.user_id == user_id)
            .first()
        )

        if account is None:
            return {
                "eligible": False,
                "user_id": user_id,
                "error": "ACCOUNT_NOT_FOUND",
            }

        reasons = []

        if account.status != "active":
            reasons.append("ACCOUNT_NOT_ACTIVE")

        if account.failed_attempts >= self.MAX_FAILED_ATTEMPTS:
            reasons.append("FAILED_ATTEMPT_LIMIT_REACHED")

        if not account.mfa_enabled:
            reasons.append("MFA_REQUIRED")

        eligible = len(reasons) == 0

        return {
            "eligible": eligible,
            "user_id": user_id,
            "account_status": account.status,
            "account_locked": account.locked,
            "mfa_enabled": account.mfa_enabled,
            "failed_attempts": account.failed_attempts,
            "reasons": reasons,
        }