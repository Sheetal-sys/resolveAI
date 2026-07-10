from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    email: EmailStr
    temporary_password: str = Field(..., min_length=8, max_length=72)
    role: str