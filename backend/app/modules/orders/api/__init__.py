
from fastapi import APIRouter

from app.modules.orders.api.create_order import (
    router as create_order_router,
)
from app.modules.orders.api.get_order import (
    router as get_order_router,
)
from app.modules.orders.api.list_orders import (
    router as list_orders_router,
)
from app.modules.orders.api.update_order import (
    router as update_order_router,
)
from app.modules.orders.api.change_order_status import (
    router as change_order_status_router,
)


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"],
)

router.include_router(create_order_router)
router.include_router(list_orders_router)
router.include_router(get_order_router)
router.include_router(update_order_router)
router.include_router(change_order_status_router)


__all__ = ["router"]
