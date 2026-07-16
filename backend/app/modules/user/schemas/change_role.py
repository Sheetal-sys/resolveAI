from pydantic import BaseModel, Field


class ChangeUserRoleRequest(BaseModel):
    role: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )