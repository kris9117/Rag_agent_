from app.services.database import SessionLocal
from app.services.device_service import DeviceService
from app.tools.schemas import DeviceIdInput


def get_device_status(device_id: str) -> dict:
    """Retrieve device status."""

    try:
        validated = DeviceIdInput(device_id=device_id)
    except ValueError as exc:
        return {
            "found": False,
            "error": "INVALID_TOOL_INPUT",
            "details": str(exc),
        }

    db = SessionLocal()

    try:
        service = DeviceService(db)
        return service.get_device_status(validated.device_id)
    finally:
        db.close()