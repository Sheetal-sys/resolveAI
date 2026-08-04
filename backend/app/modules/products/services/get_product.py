from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import ProductResponse


def get_product(
    db: Session,
    tenant_id: int,
    product_id: int,
) -> ProductResponse:
    repository = ProductRepository(db)

    product = repository.get_by_id_and_tenant(
        product_id=product_id,
        tenant_id=tenant_id,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return ProductResponse.model_validate(product)