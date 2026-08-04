from pydantic import BaseModel, EmailStr, Field

from app.shared.base.enums import CustomerSource


class CustomerUpdateRequest(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        max_length=100,
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=30,
    )

    company: str | None = Field(
        default=None,
        max_length=150,
    )

    source: CustomerSource | None = None

    internal_notes: str | None = Field(
        default=None,
        max_length=2000,
    )