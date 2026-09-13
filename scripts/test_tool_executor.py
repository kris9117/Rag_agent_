from app.agent.tool_executor import execute_tool


def main() -> None:
    print("=== Account Status ===")

    result = execute_tool(
        tool_name="ACCOUNT_STATUS",
        arguments={
            "user_id": "EMP0001",
        },
    )

    print(result)

    print("\n=== Device Status ===")

    result = execute_tool(
        tool_name="DEVICE_STATUS",
        arguments={
            "device_id": "DEV0001",
        },
    )

    print(result)

    print("\n=== Ticket Lookup ===")

    result = execute_tool(
        tool_name="TICKET_LOOKUP",
        arguments={
            "ticket_id": "INC000001",
        },
    )

    print(result)

    print("\n=== Unknown Tool ===")

    result = execute_tool(
        tool_name="DELETE_USER",
        arguments={
            "user_id": "EMP0001",
        },
    )

    print(result)


if __name__ == "__main__":
    main()