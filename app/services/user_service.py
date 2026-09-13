from sqlalchemy.orm import Session

from app.models.database_models import Employee


class UserService:
    """Business logic for employee profile operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_user_profile(self, user_id: str) -> dict:
        """Return employee profile with account and device information."""

        employee = (
            self.db.query(Employee)
            .filter(Employee.user_id == user_id)
            .first()
        )

        if employee is None:
            return {
                "found": False,
                "user_id": user_id,
                "error": "USER_NOT_FOUND",
            }

        return {
            "found": True,
            "user_id": employee.user_id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "role": employee.role,
            "employee_status": employee.status,
            "account": {
                "status": employee.account.status if employee.account else None,
                "locked": employee.account.locked if employee.account else None,
                "mfa_enabled": (
                    employee.account.mfa_enabled
                    if employee.account
                    else None
                ),
            },
            "device": {
                "device_id": employee.device.device_id
                if employee.device
                else None,
                "hostname": employee.device.hostname
                if employee.device
                else None,
                "os": employee.device.os
                if employee.device
                else None,
                "status": employee.device.status
                if employee.device
                else None,
                "vpn_status": (
                    employee.device.vpn_status
                    if employee.device
                    else None
                ),
            },
        }