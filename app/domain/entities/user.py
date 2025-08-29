from datetime import datetime

from app.models.base import Base


class User(Base):
    email: str
    password: str
    first_name: str
    last_name: str
    dob: datetime
    is_active: bool = True

    class Settings:
        name = "users"