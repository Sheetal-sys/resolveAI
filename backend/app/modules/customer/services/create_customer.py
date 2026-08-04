from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.customer.models import Customer
from app.modules.customer.repositories import CustomerRepository
from app.modules.customer.schemas import (
    CustomerCreateRequest,
    CustomerResponse,
)
from app.shared.base.enums import CustomerStatus


class CreateCustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def create_customer(
        self,
        request: CustomerCreateRequest,
        current_user: CurrentUserResponse,
    ) -> CustomerResponse:
        normalized_email = str(request.email).lower().strip()

        existing_customer = self.repository.get_by_email_and_tenant(
            email=normalized_email,
            tenant_id=current_user.tenant_id,
        )

        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A customer with this email already exists",
            )

        try:
            customer = Customer(
                tenant_id=current_user.tenant_id,
                customer_code="TEMP",
                first_name=request.first_name.strip(),
                last_name=(
                    request.last_name.strip()
                    if request.last_name
                    else None
                ),
                email=normalized_email,
                phone=(
                    request.phone.strip()
                    if request.phone
                    else None
                ),
                company=(
                    request.company.strip()
                    if request.company
                    else None
                ),
                status=CustomerStatus.ACTIVE.value,
                source=request.source.value,
                internal_notes=(
                    request.internal_notes.strip()
                    if request.internal_notes
                    else None
                ),
            )

            customer = self.repository.create(customer)

            customer.customer_code = f"CUST-{customer.id:06d}"

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
                detail=f"Customer creation failed: {str(exc)}",
            ) from exc