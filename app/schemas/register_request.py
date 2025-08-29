import re
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, field_validator


class RegisterRequest(BaseModel):
    """Request schema for user registration."""

    email: EmailStr
    password: str
    first_name: str
    last_name: str
    dob: datetime
    role: Optional[str] = "user"

    # Validate password
    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if len(v) < 7:
            raise ValueError("Password must be at least 7 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

    # Validate date of birth
    @field_validator("dob")
    def validate_dob(cls, v: datetime) -> datetime:
        today = date.today()
        dob_date = v.date()
        if dob_date > today:
            raise ValueError("Date of birth cannot be in the future")
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        if age < 13:
            raise ValueError("User must be at least 13 years old")
        return v
