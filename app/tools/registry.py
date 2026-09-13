from app.tools.account_tools import get_account_status
from app.tools.device_tools import get_device_status
from app.tools.password_tools import check_password_reset_eligibility
from app.tools.ticket_tools import create_ticket, get_ticket
from app.tools.user_tools import get_user_profile


TOOL_REGISTRY = {
    "ACCOUNT_STATUS": get_account_status,
    "DEVICE_STATUS": get_device_status,
    "TICKET_LOOKUP": get_ticket,
    "CREATE_TICKET": create_ticket,
    "PASSWORD_RESET": check_password_reset_eligibility,
    "USER_PROFILE": get_user_profile,
}