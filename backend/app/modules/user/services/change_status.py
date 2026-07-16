from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.schemas import ChangeUserStatusRequest, UserResponse


class ChangeUserStatusService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def change_status(
        self,
        user_id: int,
        request: ChangeUserStatusRequest,
        current_user: CurrentUserResponse,
    ) -> UserResponse:
        record = self.repository.get_user_by_id_and_tenant(
            user_id=user_id,
            tenant_id=current_user.tenant_id,
        )

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user, tenant_user, role = record

        if user.id == current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot change your own account status",
            )

        if tenant_user.is_active == request.is_active:
            current_status = "active" if request.is_active else "inactive"

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User is already {current_status}",
            )

        try:
            tenant_user = self.repository.update_tenant_user_status(
                tenant_user=tenant_user,
                is_active=request.is_active,
            )

            self.repository.commit()
            self.repository.refresh(tenant_user)

            return UserResponse(
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role=role.name,
                is_active=tenant_user.is_active,
                tenant_id=tenant_user.tenant_id,
                joined_at=tenant_user.joined_at,
            )

        except HTTPException:
            self.repository.rollback()
            raise

        except Exception as exc:
            self.repository.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User status update failed: {str(exc)}",
            ) from exc