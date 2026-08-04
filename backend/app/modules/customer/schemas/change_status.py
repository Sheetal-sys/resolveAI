from pydantic import BaseModel

from app.shared.base.enums import CustomerStatus


class ChangeCustomerStatusRequest(BaseModel):
    status: CustomerStatus