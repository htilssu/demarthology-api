from datetime import datetime
from typing import Optional

from app.models.base import Base


class User(Base):
    email: str
    password: str
    first_name: str
    last_name: str
    dob: datetime
    role: Optional[str] = "user"  # Default role is "user"

    class Settings:
        name = "users"
