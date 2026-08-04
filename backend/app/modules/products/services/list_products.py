from sqlalchemy.orm import Session

from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import (
    ProductListResponse,
    ProductResponse,
)


def list_products(
    db: Session,
    tenant_id: int,
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
    product_status: str | None = None,
    category: str | None = None,
) -> ProductListResponse:
    repository = ProductRepository(db)

    products, total = repository.list_by_tenant(
        tenant_id=tenant_id,
        skip=skip,
        limit=limit,
        search=search,
        product_status=product_status,
        category=category,
    )

    return ProductListResponse(
        items=[
            ProductResponse.model_validate(product)
            for product in products
        ],
        total=total,
        skip=skip,
        limit=limit,
    )