from app.tools.password_tools import check_password_reset_eligibility


def main() -> None:
    print("=== Existing User ===")

    result = check_password_reset_eligibility("EMP0001")

    print(result)

    print("\n=== Another Existing User ===")

    result = check_password_reset_eligibility("EMP0002")

    print(result)

    print("\n=== Unknown User ===")

    result = check_password_reset_eligibility("EMP9999")

    print(result)


if __name__ == "__main__":
    main()