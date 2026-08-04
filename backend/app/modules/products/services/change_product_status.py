from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import (
    ChangeProductStatusRequest,
    ProductResponse,
)


def change_product_status(
    db: Session,
    tenant_id: int,
    product_id: int,
    request: ChangeProductStatusRequest,
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

    requested_status = request.status

    if product.status == requested_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product is already {requested_status}",
        )

    try:
        product.status = requested_status

        repository.update(product)
        repository.commit()
        repository.refresh(product)

        return ProductResponse.model_validate(product)

    except HTTPException:
        repository.rollback()
        raise

    except Exception as exc:
        repository.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Product status update failed: {str(exc)}",
        ) from exc