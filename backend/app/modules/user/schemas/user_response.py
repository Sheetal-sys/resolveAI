from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str | None
    email: str
    role: str
    is_active: bool
    tenant_id: int
    joined_at: datetime