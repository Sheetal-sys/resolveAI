from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.modules.products.models import Product
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import (
    ProductCreateRequest,
    ProductResponse,
)


def create_product(
    db: Session,
    tenant_id: int,
    request: ProductCreateRequest,
) -> ProductResponse:
    """
    Create a new product for the tenant.
    """

    repository = ProductRepository(db)

    existing_product = repository.get_by_sku_and_tenant(
        sku=request.sku,
        tenant_id=tenant_id,
    )

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists.",
        )

    # Generate Product Code
    products, total = repository.list_by_tenant(
        tenant_id=tenant_id,
        skip=0,
        limit=1,
    )

    product_code = f"PROD-{total + 1:06d}"

    product = Product(
        tenant_id=tenant_id,
        product_code=product_code,
        sku=request.sku,
        name=request.name,
        description=request.description,
        category=request.category,
        brand=request.brand,
        price=request.price,
        currency=request.currency,
        stock_quantity=request.stock_quantity,
        image_url=str(request.image_url)
        if request.image_url
        else None,
    )

    try:
        repository.create(product)
        repository.commit()
        repository.refresh(product)

    except IntegrityError:
        repository.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists.",
        )

    return ProductResponse.model_validate(product)