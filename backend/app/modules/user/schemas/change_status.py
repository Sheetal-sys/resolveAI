from pydantic import BaseModel


class ChangeUserStatusRequest(BaseModel):
    is_active: bool