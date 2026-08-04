from fastapi import APIRouter

from app.modules.customer.api.change_status import (
    router as change_status_router,
)
from app.modules.customer.api.create_customer import (
    router as create_customer_router,
)
from app.modules.customer.api.get_customer import (
    router as get_customer_router,
)
from app.modules.customer.api.list_customers import (
    router as list_customers_router,
)
from app.modules.customer.api.update_customer import (
    router as update_customer_router,
)

from app.modules.customer.api.remove_customer import (
    router as remove_customer_router,
)

router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customers"],
)

router.include_router(create_customer_router)
router.include_router(list_customers_router)
router.include_router(get_customer_router)
router.include_router(update_customer_router)
router.include_router(change_status_router)
router.include_router(remove_customer_router)

__all__ = ["router"]