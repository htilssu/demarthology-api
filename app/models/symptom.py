from typing import Optional

from app.models.base import Base


class Symptom(Base):
    name: str
    description: Optional[str] = None

    class Settings:
        name = "symptoms"
