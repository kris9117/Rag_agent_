from pydantic import BaseModel, Field


class SupportRequest(BaseModel):
    user_id: str | None = Field(
        default=None,
        description="Employee ID, for example EMP0001.",
    )
    query: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Employee IT support request.",
    )


class SupportResponse(BaseModel):
    request_id: str
    user_id: str | None
    intent: str | None
    route: str | None
    status: str | None
    response: str | None
    escalation_required: bool