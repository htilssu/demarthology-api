from pydantic import BaseModel, field_validator


class ResetPasswordRequest(BaseModel):
    """Request schema for reset password endpoint."""

    token: str
    new_password: str
    confirm_new_password: str

    @field_validator("confirm_new_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Passwords do not match")
        return v
