from typing import Optional

from app.models.base import Base


class Role(Base):
    name: str
    description: Optional[str] = None
    is_active: bool = True

    class Settings:
        name = "roles"
