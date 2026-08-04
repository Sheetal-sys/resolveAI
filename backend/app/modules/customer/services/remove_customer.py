from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository


class RemoveCustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def remove_customer(
        self,
        customer_id: int,
        current_user: CurrentUserResponse,
    ) -> dict[str, str]:
        customer = self.repository.get_by_id_and_tenant(
            customer_id=customer_id,
            tenant_id=current_user.tenant_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        try:
            self.repository.delete(customer)
            self.repository.commit()

            return {
                "message": "Customer deleted successfully",
            }

        except HTTPException:
            self.repository.rollback()
            raise

        except Exception as exc:
            self.repository.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Customer deletion failed: {str(exc)}",
            ) from exc