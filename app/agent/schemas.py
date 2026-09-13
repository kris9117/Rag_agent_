from typing import Literal

from pydantic import BaseModel, Field


class RequestEntities(BaseModel):
    """Entities explicitly extracted from the employee request."""

    user_id: str | None = Field(
        default=None,
        description="Employee ID such as EMP0001, or null if not provided.",
    )

    device_id: str | None = Field(
        default=None,
        description="Device ID such as DEV0001, or null if not provided.",
    )

    ticket_id: str | None = Field(
        default=None,
        description="Ticket ID such as INC000001, or null if not provided.",
    )

    category: str | None = Field(
        default=None,
        description=(
            "Ticket category such as Hardware, Software, "
            "Network, Access, or Security."
        ),
    )

    priority: Literal["low", "medium", "high"] | None = Field(
        default=None,
        description="Ticket priority: low, medium, or high.",
    )

    description: str | None = Field(
        default=None,
        description="Detailed description of the IT issue.",
    )


class RequestUnderstanding(BaseModel):
    """Structured interpretation of an employee IT request."""

    intent: Literal[
        "KNOWLEDGE",
        "ACCOUNT_STATUS",
        "DEVICE_STATUS",
        "TICKET_LOOKUP",
        "CREATE_TICKET",
        "PASSWORD_RESET",
        "VPN_TROUBLESHOOTING",
        "ESCALATION",
        "CLARIFICATION",
    ]

    entities: RequestEntities

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    missing_information: list[str] = Field(
        default_factory=list,
    )