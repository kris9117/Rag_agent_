from app.tools.account_tools import get_account_status


def main() -> None:
    print("=== Existing User ===")
    print(get_account_status("EMP0001"))

    print("\n=== Unknown User ===")
    print(get_account_status("EMP9999"))


if __name__ == "__main__":
    main()