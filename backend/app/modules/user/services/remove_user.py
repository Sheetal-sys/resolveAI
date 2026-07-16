from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.user.repositories.user_repository import UserRepository


class RemoveUserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def remove_user(
        self,
        user_id: int,
        current_user: CurrentUserResponse,
    ) -> dict[str, str]:
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
                detail="You cannot remove your own tenant membership",
            )

        try:
            self.repository.delete_tenant_user(tenant_user)
            self.repository.commit()

            return {
                "message": "User removed from tenant successfully",
            }

        except HTTPException:
            self.repository.rollback()
            raise

        except Exception as exc:
            self.repository.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User removal failed: {str(exc)}",
            ) from exc