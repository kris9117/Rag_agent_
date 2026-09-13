from app.services.database import SessionLocal
from app.services.user_service import UserService


def main() -> None:
    db = SessionLocal()

    try:
        service = UserService(db)

        print("=== Existing User ===")
        result = service.get_user_profile("EMP0001")
        print(result)

        print("\n=== Unknown User ===")
        result = service.get_user_profile("EMP9999")
        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    main()