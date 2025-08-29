from datetime import datetime
from typing import Optional

from app.models.base import Base
from app.models.role import Role


class User(Base):
    email: str
    password: str
    first_name: str
    last_name: str
    dob: datetime
    role: Optional[list[Role]] = None

    class Settings:
        name = "users"
