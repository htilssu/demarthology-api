from datetime import datetime

from beanie import Document


class User(Document):
    email: str
    password: str
    first_name: str
    last_name: str
    dob: datetime

    class Settings:
        name = "users"
