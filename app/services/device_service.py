from sqlalchemy.orm import Session

from app.models.database_models import Device


class DeviceService:
    """Business logic for device operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_device_status(self, device_id: str) -> dict:
        """Return the current status of a device."""

        device = (
            self.db.query(Device)
            .filter(Device.device_id == device_id)
            .first()
        )

        if device is None:
            return {
                "found": False,
                "device_id": device_id,
                "error": "DEVICE_NOT_FOUND",
            }

        return {
            "found": True,
            "device_id": device.device_id,
            "hostname": device.hostname,
            "os": device.os,
            "status": device.status,
            "vpn_status": device.vpn_status,
            "last_seen": device.last_seen.isoformat(),
        }