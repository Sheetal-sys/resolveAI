from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.modules.orders.models import Order, OrderItem


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------------
    # Read operations
    # ---------------------------------------------------------

    def get_by_id_and_tenant(
        self,
        order_id: int,
        tenant_id: int,
    ) -> Order | None:
        return (
            self.db.query(Order)
            .options(joinedload(Order.items))
            .filter(
                Order.id == order_id,
                Order.tenant_id == tenant_id,
            )
            .first()
        )

    def get_by_number_and_tenant(
        self,
        order_number: str,
        tenant_id: int,
    ) -> Order | None:
        return (
            self.db.query(Order)
            .filter(
                Order.order_number == order_number,
                Order.tenant_id == tenant_id,
            )
            .first()
        )

    def list_by_tenant(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        order_status: str | None = None,
        customer_id: int | None = None,
    ) -> tuple[list[Order], int]:
        query = (
            self.db.query(Order)
            .options(joinedload(Order.items))
            .filter(Order.tenant_id == tenant_id)
        )

        if search:
            search_value = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Order.order_number.ilike(search_value),
                    Order.status.ilike(search_value),
                    Order.currency.ilike(search_value),
                )
            )

        if order_status:
            query = query.filter(Order.status == order_status)

        if customer_id is not None:
            query = query.filter(Order.customer_id == customer_id)

        total = query.count()

        orders = (
            query.order_by(Order.ordered_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return orders, total

    # ---------------------------------------------------------
    # Write operations
    # ---------------------------------------------------------

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.flush()
        return order

    def create_item(self, item: OrderItem) -> OrderItem:
        self.db.add(item)
        self.db.flush()
        return item

    def update(self, order: Order) -> Order:
        self.db.add(order)
        self.db.flush()
        return order

    def delete(self, order: Order) -> None:
        self.db.delete(order)
        self.db.flush()

    # ---------------------------------------------------------
    # Transaction operations
    # ---------------------------------------------------------

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(self, order: Order) -> None:
        self.db.refresh(order)
        # Ensure items are loaded after refresh
        for item in order.items:
            self.db.refresh(item)
