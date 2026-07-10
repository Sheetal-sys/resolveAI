from pydantic import BaseModel

from app.modules.user.schemas.user_response import UserResponse


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    skip: int
    limit: int