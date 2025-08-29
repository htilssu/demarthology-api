from datetime import datetime

from models.base import Base


class User(Base):
    email: str
    password: str
    first_name: str
    last_name: str
    dob: datetime

    class Settings:
        name = "users"
