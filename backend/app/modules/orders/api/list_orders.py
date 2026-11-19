
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import OrderListResponse
from app.modules.orders.services.list_orders import ListOrdersService
from app.shared.base.enums import OrderStatus


router = APIRouter()


@router.get(
    "/",
    response_model=OrderListResponse,
    status_code=status.HTTP_200_OK,
)
def list_orders_endpoint(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, max_length=100),
    order_status: OrderStatus | None = Query(default=None),
    customer_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse = Depends(get_current_user),
):
    repository = OrderRepository(db)
    service = ListOrdersService(repository=repository)

    return service.list_orders(
        current_user=current_user,
        skip=skip,
        limit=limit,
        search=search,
        order_status=order_status.value if order_status is not None else None,
        customer_id=customer_id,
    )
