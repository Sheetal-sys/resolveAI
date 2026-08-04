from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.modules.customer.models import Customer


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------------
    # Read operations
    # ---------------------------------------------------------

    def get_by_id_and_tenant(
        self,
        customer_id: int,
        tenant_id: int,
    ) -> Customer | None:
        return (
            self.db.query(Customer)
            .filter(
                Customer.id == customer_id,
                Customer.tenant_id == tenant_id,
            )
            .first()
        )

    def get_by_email_and_tenant(
        self,
        email: str,
        tenant_id: int,
    ) -> Customer | None:
        return (
            self.db.query(Customer)
            .filter(
                Customer.email == email,
                Customer.tenant_id == tenant_id,
            )
            .first()
        )

    def get_by_code_and_tenant(
        self,
        customer_code: str,
        tenant_id: int,
    ) -> Customer | None:
        return (
            self.db.query(Customer)
            .filter(
                Customer.customer_code == customer_code,
                Customer.tenant_id == tenant_id,
            )
            .first()
        )

    def list_by_tenant(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        customer_status: str | None = None,
        source: str | None = None,
    ) -> tuple[list[Customer], int]:
        query = (
            self.db.query(Customer)
            .filter(Customer.tenant_id == tenant_id)
        )

        if search:
            search_value = f"%{search.strip()}%"

            query = query.filter(
                or_(
                    Customer.customer_code.ilike(search_value),
                    Customer.first_name.ilike(search_value),
                    Customer.last_name.ilike(search_value),
                    Customer.email.ilike(search_value),
                    Customer.phone.ilike(search_value),
                    Customer.company.ilike(search_value),
                )
            )

        if customer_status:
            query = query.filter(
                Customer.status == customer_status
            )

        if source:
            query = query.filter(
                Customer.source == source
            )

        total = query.count()

        customers = (
            query.order_by(Customer.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return customers, total

    # ---------------------------------------------------------
    # Write operations
    # ---------------------------------------------------------

    def create(
        self,
        customer: Customer,
    ) -> Customer:
        self.db.add(customer)
        self.db.flush()

        return customer

    def update(
        self,
        customer: Customer,
    ) -> Customer:
        self.db.add(customer)
        self.db.flush()

        return customer

    def delete(
        self,
        customer: Customer,
    ) -> None:
        self.db.delete(customer)
        self.db.flush()

    # ---------------------------------------------------------
    # Transaction operations
    # ---------------------------------------------------------

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(
        self,
        customer: Customer,
    ) -> None:
        self.db.refresh(customer)