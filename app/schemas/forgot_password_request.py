from pydantic import BaseModel, EmailStr


class ForgotPasswordRequest(BaseModel):
    """Request schema for forgot password endpoint."""

    email: EmailStr
