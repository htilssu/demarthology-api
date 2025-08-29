from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """Request schema for user registration."""

    email: EmailStr
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    dob: datetime
    role: Optional[str] = "user"
