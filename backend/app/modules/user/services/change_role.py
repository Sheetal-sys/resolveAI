from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository
from app.modules.user.schemas import ChangeUserRoleRequest, UserResponse
from app.shared.base.enums import RoleName


class ChangeUserRoleService:
    ALLOWED_ROLES = {
        RoleName.SUPERVISOR.value,
        RoleName.SUPPORT_AGENT.value,
    }

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def change_role(
        self,
        user_id: int,
        request: ChangeUserRoleRequest,
        current_user: CurrentUserResponse,
    ) -> UserResponse:
        requested_role = request.role.upper().strip()

        if requested_role not in self.ALLOWED_ROLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid role. Allowed roles are "
                    "SUPERVISOR and SUPPORT_AGENT."
                ),
            )

        record = self.repository.get_user_by_id_and_tenant(
            user_id=user_id,
            tenant_id=current_user.tenant_id,
        )

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user, tenant_user, current_role = record

        if user.id == current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot change your own role",
            )

        new_role = self.repository.get_role_by_name(requested_role)

        if new_role is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Role {requested_role} was not found",
            )

        if tenant_user.role_id == new_role.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User already has role {requested_role}",
            )

        try:
            tenant_user = self.repository.update_tenant_user_role(
                tenant_user=tenant_user,
                role_id=new_role.id,
            )

            self.repository.commit()
            self.repository.refresh(tenant_user)

            return UserResponse(
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role=new_role.name,
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
                detail=f"Role update failed: {str(exc)}",
            ) from exc