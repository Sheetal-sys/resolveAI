from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import OrderResponse


class GetOrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def get_order(
        self,
        order_id: int,
        current_user: CurrentUserResponse,
    ) -> OrderResponse:
        order = self.repository.get_by_id_and_tenant(
            order_id=order_id,
            tenant_id=current_user.tenant_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        return OrderResponse.model_validate(order)
