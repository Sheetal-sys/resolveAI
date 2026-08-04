from fastapi import APIRouter

from app.modules.products.api.change_product_status import (
    router as change_product_status_router,
)
from app.modules.products.api.create_product import (
    router as create_product_router,
)
from app.modules.products.api.delete_product import (
    router as delete_product_router,
)
from app.modules.products.api.get_product import (
    router as get_product_router,
)
from app.modules.products.api.list_products import (
    router as list_products_router,
)
from app.modules.products.api.update_product import (
    router as update_product_router,
)

router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"],
)

router.include_router(create_product_router)
router.include_router(list_products_router)
router.include_router(get_product_router)
router.include_router(update_product_router)
router.include_router(change_product_status_router)
router.include_router(delete_product_router)

__all__ = ["router"]