from app.tools.device_tools import get_device_status


def main() -> None:
    print("=== Existing Device ===")
    print(get_device_status("DEV0001"))

    print("\n=== Unknown Device ===")
    print(get_device_status("DEV9999"))


if __name__ == "__main__":
    main()