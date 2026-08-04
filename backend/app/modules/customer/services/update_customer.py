from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.schemas import (
    CustomerResponse,
    CustomerUpdateRequest,
)


class UpdateCustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def update_customer(
        self,
        customer_id: int,
        request: CustomerUpdateRequest,
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

        update_data = request.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields were provided for update",
            )

        if "email" in update_data:
            normalized_email = str(update_data["email"]).lower().strip()

            existing_customer = self.repository.get_by_email_and_tenant(
                email=normalized_email,
                tenant_id=current_user.tenant_id,
            )

            if (
                existing_customer is not None
                and existing_customer.id != customer.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A customer with this email already exists",
                )

            customer.email = normalized_email

        if "first_name" in update_data:
            customer.first_name = update_data["first_name"].strip()

        if "last_name" in update_data:
            value = update_data["last_name"]
            customer.last_name = value.strip() if value else None

        if "phone" in update_data:
            value = update_data["phone"]
            customer.phone = value.strip() if value else None

        if "company" in update_data:
            value = update_data["company"]
            customer.company = value.strip() if value else None

        if "source" in update_data:
            customer.source = update_data["source"].value

        if "internal_notes" in update_data:
            value = update_data["internal_notes"]
            customer.internal_notes = value.strip() if value else None

        try:
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
                detail=f"Customer update failed: {str(exc)}",
            ) from exc