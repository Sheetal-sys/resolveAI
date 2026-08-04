from pydantic import BaseModel

from app.modules.customer.schemas.customer_response import CustomerResponse


class CustomerListResponse(BaseModel):
    items: list[CustomerResponse]
    total: int
    skip: int
    limit: int