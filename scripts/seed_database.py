import random
from datetime import datetime, timedelta

from app.models.database_models import Account, Device, Employee, Ticket
from app.services.database import SessionLocal, create_tables


DEPARTMENTS = [
    "Engineering",
    "Finance",
    "Human Resources",
    "Sales",
    "Operations",
    "Marketing",
    "IT",
]

ROLES = [
    "Software Engineer",
    "Business Analyst",
    "Manager",
    "Data Analyst",
    "HR Specialist",
    "Sales Executive",
    "Operations Analyst",
]


def seed_database() -> None:
    create_tables()

    db = SessionLocal()

    try:
        existing_employee = db.query(Employee).first()

        if existing_employee:
            print("Database already contains data. Skipping seed.")
            return

        employees = []
        devices = []
        accounts = []

        now = datetime.utcnow()

        for index in range(1, 51):
            user_id = f"EMP{index:04d}"
            device_id = f"DEV{index:04d}"

            employee = Employee(
                user_id=user_id,
                name=f"Employee {index:04d}",
                email=f"employee{index:04d}@enterprise.local",
                department=random.choice(DEPARTMENTS),
                role=random.choice(ROLES),
                status="active",
                device_id=device_id,
            )

            device = Device(
                device_id=device_id,
                hostname=f"LAPTOP-{index:04d}",
                os=random.choice(
                    [
                        "Windows 11",
                        "Windows 11",
                        "macOS 15",
                    ]
                ),
                status=random.choice(
                    [
                        "healthy",
                        "healthy",
                        "healthy",
                        "warning",
                    ]
                ),
                vpn_status=random.choice(
                    [
                        "connected",
                        "connected",
                        "disconnected",
                    ]
                ),
                last_seen=now - timedelta(
                    minutes=random.randint(1, 180)
                ),
            )

            account = Account(
                user_id=user_id,
                status="active",
                locked=random.choice(
                    [
                        False,
                        False,
                        False,
                        True,
                    ]
                ),
                mfa_enabled=True,
                failed_attempts=random.randint(0, 5),
                password_last_changed=now - timedelta(
                    days=random.randint(1, 180)
                ),
            )

            employees.append(employee)
            devices.append(device)
            accounts.append(account)

        db.add_all(devices)
        db.flush()

        db.add_all(employees)
        db.flush()

        db.add_all(accounts)

        for index in range(1, 76):
            user_id = f"EMP{random.randint(1, 50):04d}"

            ticket = Ticket(
                ticket_id=f"INC{index:06d}",
                user_id=user_id,
                category=random.choice(
                    [
                        "VPN",
                        "Account",
                        "Device",
                        "Email",
                        "Software",
                    ]
                ),
                priority=random.choice(
                    [
                        "low",
                        "medium",
                        "medium",
                        "high",
                    ]
                ),
                description=random.choice(
                    [
                        "Unable to connect to VPN",
                        "Account appears to be locked",
                        "Laptop performance issue",
                        "Email synchronization problem",
                        "Software installation request",
                    ]
                ),
                status=random.choice(
                    [
                        "open",
                        "in_progress",
                        "resolved",
                    ]
                ),
                created_at=now - timedelta(
                    days=random.randint(1, 90)
                ),
                updated_at=now - timedelta(
                    days=random.randint(0, 30)
                ),
            )

            db.add(ticket)

        db.commit()

        print("Database seeded successfully.")
        print("Employees: 50")
        print("Accounts: 50")
        print("Devices: 50")
        print("Tickets: 75")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()