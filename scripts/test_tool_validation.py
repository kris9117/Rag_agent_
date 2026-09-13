from app.tools.ticket_tools import create_ticket


def main() -> None:
    print("=== Valid Input ===")

    result = create_ticket(
        user_id="EMP0001",
        category="VPN",
        description="Unable to connect to corporate VPN.",
        priority="high",
    )

    print(result)

    print("\n=== Invalid User ID ===")

    result = create_ticket(
        user_id="EMP01",
        category="VPN",
        description="Unable to connect to corporate VPN.",
        priority="high",
    )

    print(result)

    print("\n=== Invalid Category ===")

    result = create_ticket(
        user_id="EMP0001",
        category="Printer",
        description="Unable to print documents from my laptop.",
        priority="medium",
    )

    print(result)

    print("\n=== Invalid Priority ===")

    result = create_ticket(
        user_id="EMP0001",
        category="VPN",
        description="Unable to connect to corporate VPN.",
        priority="urgent",
    )

    print(result)

    print("\n=== Description Too Short ===")

    result = create_ticket(
        user_id="EMP0001",
        category="VPN",
        description="VPN",
        priority="medium",
    )

    print(result)


if __name__ == "__main__":
    main()