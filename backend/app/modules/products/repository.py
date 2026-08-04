from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.modules.products.models import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_and_tenant(
        self,
        product_id: int,
        tenant_id: int,
    ) -> Product | None:
        return (
            self.db.query(Product)
            .filter(
                Product.id == product_id,
                Product.tenant_id == tenant_id,
            )
            .first()
        )

    def get_by_sku_and_tenant(
        self,
        sku: str,
        tenant_id: int,
    ) -> Product | None:
        return (
            self.db.query(Product)
            .filter(
                Product.sku == sku,
                Product.tenant_id == tenant_id,
            )
            .first()
        )

    def get_by_code_and_tenant(
        self,
        product_code: str,
        tenant_id: int,
    ) -> Product | None:
        return (
            self.db.query(Product)
            .filter(
                Product.product_code == product_code,
                Product.tenant_id == tenant_id,
            )
            .first()
        )

    def list_by_tenant(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        product_status: str | None = None,
        category: str | None = None,
    ) -> tuple[list[Product], int]:
        query = (
            self.db.query(Product)
            .filter(Product.tenant_id == tenant_id)
        )

        if search:
            search_value = f"%{search.strip()}%"

            query = query.filter(
                or_(
                    Product.product_code.ilike(search_value),
                    Product.sku.ilike(search_value),
                    Product.name.ilike(search_value),
                    Product.description.ilike(search_value),
                    Product.category.ilike(search_value),
                    Product.brand.ilike(search_value),
                )
            )

        if product_status:
            query = query.filter(
                Product.status == product_status,
            )

        if category:
            query = query.filter(
                Product.category.ilike(category.strip()),
            )

        total = query.count()

        products = (
            query.order_by(Product.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return products, total

    def create(
        self,
        product: Product,
    ) -> Product:
        self.db.add(product)
        self.db.flush()

        return product

    def update(
        self,
        product: Product,
    ) -> Product:
        self.db.add(product)
        self.db.flush()

        return product

    def delete(
        self,
        product: Product,
    ) -> None:
        self.db.delete(product)
        self.db.flush()

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(
        self,
        product: Product,
    ) -> None:
        self.db.refresh(product)