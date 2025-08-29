from pydantic import BaseModel


class ForgotPasswordResponse(BaseModel):
    """Response schema for forgot password."""

    success: bool
    message: str


class ResetPasswordResponse(BaseModel):
    """Response schema for reset password."""

    success: bool
    message: str


class LogoutResponse(BaseModel):
    """Response schema for logout."""

    success: bool
    message: str
