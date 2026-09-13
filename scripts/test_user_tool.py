from app.tools.user_tools import get_user_profile


def main() -> None:
    print("=== Existing User ===")
    print(get_user_profile("EMP0001"))

    print("\n=== Unknown User ===")
    print(get_user_profile("EMP9999"))


if __name__ == "__main__":
    main()