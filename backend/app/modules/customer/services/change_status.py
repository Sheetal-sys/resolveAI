from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.schemas import (
    ChangeCustomerStatusRequest,
    CustomerResponse,
)


class ChangeCustomerStatusService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def change_status(
        self,
        customer_id: int,
        request: ChangeCustomerStatusRequest,
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

        requested_status = request.status.value

        if customer.status == requested_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer is already {requested_status}",
            )

        try:
            customer.status = requested_status

            customer = self.repository.update(customer)
            self.repository.commit()
            self.repository.refresh(customer)

            return CustomerResponse.model_validate(customer)

        except HTTPException:
            self.repository.rollback()
            raise

        except Exception as exc:
            self.repository.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Customer status update failed: {str(exc)}",
            ) from exc