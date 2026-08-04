from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import (
    ProductResponse,
    ProductUpdateRequest,
)


def update_product(
    db: Session,
    tenant_id: int,
    product_id: int,
    request: ProductUpdateRequest,
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

    update_data = request.model_dump(
        exclude_unset=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields were provided for update",
        )

    if "sku" in update_data:
        normalized_sku = update_data["sku"].strip()

        existing_product = repository.get_by_sku_and_tenant(
            sku=normalized_sku,
            tenant_id=tenant_id,
        )

        if (
            existing_product is not None
            and existing_product.id != product.id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A product with this SKU already exists.",
            )

        product.sku = normalized_sku

    if "name" in update_data:
        product.name = update_data["name"].strip()

    if "description" in update_data:
        value = update_data["description"]
        product.description = value.strip() if value else None

    if "category" in update_data:
        value = update_data["category"]
        product.category = value.strip() if value else None

    if "brand" in update_data:
        value = update_data["brand"]
        product.brand = value.strip() if value else None

    if "price" in update_data:
        product.price = update_data["price"]

    if "currency" in update_data:
        product.currency = update_data["currency"].upper().strip()

    if "stock_quantity" in update_data:
        product.stock_quantity = update_data["stock_quantity"]

    if "image_url" in update_data:
        value = update_data["image_url"]
        product.image_url = str(value) if value else None

    try:
        repository.update(product)
        repository.commit()
        repository.refresh(product)

        return ProductResponse.model_validate(product)

    except HTTPException:
        repository.rollback()
        raise

    except IntegrityError as exc:
        repository.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists.",
        ) from exc

    except Exception as exc:
        repository.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Product update failed: {str(exc)}",
        ) from exc