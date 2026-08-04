from pydantic import BaseModel, EmailStr, Field

from app.shared.base.enums import CustomerSource


class CustomerCreateRequest(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        max_length=100,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=30,
    )

    company: str | None = Field(
        default=None,
        max_length=150,
    )

    source: CustomerSource = CustomerSource.WEBSITE

    internal_notes: str | None = Field(
        default=None,
        max_length=2000,
    )