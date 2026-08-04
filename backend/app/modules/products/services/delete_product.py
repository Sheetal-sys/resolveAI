from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.products.repository import ProductRepository


def delete_product(
    db: Session,
    tenant_id: int,
    product_id: int,
) -> dict[str, str]:
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

    try:
        repository.delete(product)
        repository.commit()

        return {
            "message": "Product deleted successfully",
        }

    except HTTPException:
        repository.rollback()
        raise

    except Exception as exc:
        repository.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Product deletion failed: {str(exc)}",
        ) from exc