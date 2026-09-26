from pydantic import BaseModel, Field

from app.shared.base.enums import OrderStatus


class ChangeOrderStatusRequest(BaseModel):
    status: OrderStatus = Field(
        ...,
        description="New order status",
    )
