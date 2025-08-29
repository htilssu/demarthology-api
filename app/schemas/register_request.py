from datetime import datetime

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """Request schema for user registration."""
    
    email: str
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    dob: datetime