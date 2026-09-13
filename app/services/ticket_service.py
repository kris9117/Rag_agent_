from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.database_models import Employee, Ticket


class TicketService:
    """Business logic for ticket operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_ticket(self, ticket_id: str) -> dict:
        """Return ticket details for a given ticket ID."""

        ticket = (
            self.db.query(Ticket)
            .filter(Ticket.ticket_id == ticket_id)
            .first()
        )

        if ticket is None:
            return {
                "found": False,
                "ticket_id": ticket_id,
                "error": "TICKET_NOT_FOUND",
            }

        return {
            "found": True,
            "ticket_id": ticket.ticket_id,
            "user_id": ticket.user_id,
            "category": ticket.category,
            "priority": ticket.priority,
            "description": ticket.description,
            "status": ticket.status,
            "created_at": ticket.created_at.isoformat(),
            "updated_at": ticket.updated_at.isoformat(),
        }

    def create_ticket(
        self,
        user_id: str,
        category: str,
        description: str,
        priority: str = "medium",
    ) -> dict:
        """Create a new IT support ticket."""

        employee = (
            self.db.query(Employee)
            .filter(Employee.user_id == user_id)
            .first()
        )

        if employee is None:
            return {
                "created": False,
                "user_id": user_id,
                "error": "USER_NOT_FOUND",
            }

        ticket_id = f"INC{self._next_ticket_number():06d}"

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        ticket = Ticket(
            ticket_id=ticket_id,
            user_id=user_id,
            category=category,
            priority=priority,
            description=description,
            status="open",
            created_at=now,
            updated_at=now,
        )

        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)

        return {
            "created": True,
            "ticket_id": ticket.ticket_id,
            "user_id": ticket.user_id,
            "category": ticket.category,
            "priority": ticket.priority,
            "description": ticket.description,
            "status": ticket.status,
            "created_at": ticket.created_at.isoformat(),
        }

    def _next_ticket_number(self) -> int:
        """Return the next available numeric ticket identifier."""

        tickets = self.db.query(Ticket.ticket_id).all()

        numbers = []

        for (ticket_id,) in tickets:
            try:
                numbers.append(int(ticket_id.replace("INC", "")))
            except ValueError:
                continue

        return max(numbers, default=0) + 1