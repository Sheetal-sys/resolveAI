
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import OrderResponse
from app.modules.orders.services.get_order import GetOrderService


router = APIRouter()


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
def get_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse = Depends(get_current_user),
):
    repository = OrderRepository(db)

    service = GetOrderService(repository=repository)

    return service.get_order(
        order_id=order_id,
        current_user=current_user,
    )
