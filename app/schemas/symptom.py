from typing import Optional

from pydantic import BaseModel


class SymptomCreate(BaseModel):
    name: str
    description: Optional[str] = None


class SymptomUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
