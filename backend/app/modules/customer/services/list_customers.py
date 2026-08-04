from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.schemas import (
    CustomerListResponse,
    CustomerResponse,
)
from app.shared.base.enums import CustomerSource, CustomerStatus


class ListCustomersService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def list_customers(
        self,
        current_user: CurrentUserResponse,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        customer_status: CustomerStatus | None = None,
        source: CustomerSource | None = None,
    ) -> CustomerListResponse:
        customers, total = self.repository.list_by_tenant(
            tenant_id=current_user.tenant_id,
            skip=skip,
            limit=limit,
            search=search,
            customer_status=(
                customer_status.value
                if customer_status is not None
                else None
            ),
            source=(
                source.value
                if source is not None
                else None
            ),
        )

        return CustomerListResponse(
            items=[
                CustomerResponse.model_validate(customer)
                for customer in customers
            ],
            total=total,
            skip=skip,
            limit=limit,
        )