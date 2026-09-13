from app.tools.ticket_tools import get_ticket


def main() -> None:
    print("=== Existing Ticket ===")
    print(get_ticket("INC000001"))

    print("\n=== Unknown Ticket ===")
    print(get_ticket("INC999999"))


if __name__ == "__main__":
    main()