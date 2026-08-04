from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.schemas import CustomerResponse


class GetCustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_customer(
        self,
        customer_id: int,
        current_user: CurrentUserResponse,
    ) -> CustomerResponse:
        customer = self.repository.get_by_id_and_tenant(
            customer_id=customer_id,
            tenant_id=current_user.tenant_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        return CustomerResponse.model_validate(customer)