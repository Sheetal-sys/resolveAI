from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.shared.base.enums import CustomerSource, CustomerStatus


class CustomerResponse(BaseModel):
    id: int
    customer_code: str

    first_name: str
    last_name: str | None

    email: str
    phone: str | None

    company: str | None

    status: CustomerStatus
    source: CustomerSource

    internal_notes: str | None

    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )