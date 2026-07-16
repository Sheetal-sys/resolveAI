from pydantic import BaseModel, Field


class ResetUserPasswordRequest(BaseModel):
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=72,
    )