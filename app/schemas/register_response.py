from pydantic import BaseModel

from app.schemas.login_response import UserInfo


class RegisterResponse(BaseModel):
    """Response schema for successful registration."""

    success: bool
    message: str
    user: UserInfo
