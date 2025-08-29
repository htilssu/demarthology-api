from pydantic import BaseModel


class UserInfo(BaseModel):
    """User information returned in login response."""

    email: str
    first_name: str
    last_name: str


class LoginResponse(BaseModel):
    """Response schema for successful login."""

    success: bool
    message: str
    user: UserInfo
