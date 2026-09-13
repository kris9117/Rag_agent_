from app.tools.account_tools import get_account_status
from app.tools.device_tools import get_device_status
from app.tools.ticket_tools import get_ticket
from app.tools.user_tools import get_user_profile


def main() -> None:
    print("=== Invalid User ID ===")
    print(get_user_profile("BAD001"))

    print("\n=== Invalid Account ID ===")
    print(get_account_status("EMP01"))

    print("\n=== Invalid Device ID ===")
    print(get_device_status("DEVICE01"))

    print("\n=== Invalid Ticket ID ===")
    print(get_ticket("TICKET01"))


if __name__ == "__main__":
    main()