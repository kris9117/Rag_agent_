from app.tools.ticket_tools import create_ticket, get_ticket


def main() -> None:
    print("=== Create Ticket ===")

    result = create_ticket(
        user_id="EMP0001",
        category="VPN",
        description="Unable to connect to corporate VPN.",
        priority="high",
    )

    print(result)

    if result.get("created"):
        ticket_id = result["ticket_id"]

        print("\n=== Verify Created Ticket ===")
        print(get_ticket(ticket_id))

    print("\n=== Unknown User ===")

    result = create_ticket(
        user_id="EMP9999",
        category="VPN",
        description="Unable to connect to corporate VPN.",
        priority="high",
    )

    print(result)


if __name__ == "__main__":
    main()