from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """Request schema for user registration."""

    email: EmailStr
    password: str
    first_name: str
    last_name: str
    dob: datetime
