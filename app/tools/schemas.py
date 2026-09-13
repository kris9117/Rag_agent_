from typing import Literal

from pydantic import BaseModel, Field


class UserIdInput(BaseModel):
    user_id: str = Field(
        ...,
        pattern=r"^EMP\d{4}$",
        description="Enterprise employee ID, for example EMP0001.",
    )


class DeviceIdInput(BaseModel):
    device_id: str = Field(
        ...,
        pattern=r"^DEV\d{4}$",
        description="Enterprise device ID, for example DEV0001.",
    )


class TicketIdInput(BaseModel):
    ticket_id: str = Field(
        ...,
        pattern=r"^INC\d{6}$",
        description="Enterprise incident ID, for example INC000001.",
    )


class CreateTicketInput(BaseModel):
    user_id: str = Field(
        ...,
        pattern=r"^EMP\d{4}$",
        description="Enterprise employee ID.",
    )

    category: Literal[
        "VPN",
        "Account",
        "Device",
        "Email",
        "Software",
    ]

    description: str = Field(
        ...,
        min_length=10,
        max_length=1000,
    )

    priority: Literal[
        "low",
        "medium",
        "high",
    ] = "medium"