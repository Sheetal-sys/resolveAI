from pydantic import BaseModel

from app.modules.orders.schemas.order_response import OrderResponse


class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    skip: int
    limit: int
