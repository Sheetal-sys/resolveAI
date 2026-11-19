
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import OrderCreateRequest, OrderResponse
from app.modules.orders.services.create_order import CreateOrderService
from app.modules.products.repository import ProductRepository
from app.shared.base.enums import RoleName


router = APIRouter()


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order_endpoint(
    request: OrderCreateRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse = Depends(
        require_roles(
            [
                RoleName.TENANT_ADMIN.value,
                RoleName.SUPERVISOR.value,
            ]
        )
    ),
):
    order_repository = OrderRepository(db)
    customer_repository = CustomerRepository(db)
    product_repository = ProductRepository(db)

    service = CreateOrderService(
        order_repository=order_repository,
        customer_repository=customer_repository,
        product_repository=product_repository,
    )

    return service.create_order(
        request=request,
        current_user=current_user,
    )
