from app.modules.auth.schemas import CurrentUserResponse
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import OrderListResponse, OrderResponse


class ListOrdersService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def list_orders(
        self,
        current_user: CurrentUserResponse,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        order_status: str | None = None,
        customer_id: int | None = None,
    ) -> OrderListResponse:
        orders, total = self.repository.list_by_tenant(
            tenant_id=current_user.tenant_id,
            skip=skip,
            limit=limit,
            search=search,
            order_status=order_status,
            customer_id=customer_id,
        )

        return OrderListResponse(
            items=[OrderResponse.model_validate(o) for o in orders],
            total=total,
            skip=skip,
            limit=limit,
        )
