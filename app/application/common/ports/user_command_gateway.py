from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.user import User


class UserCommandGateway(ABC):
    """Port for user data operations"""
    
    @abstractmethod
    async def read_by_id(self, user_id: str) -> Optional[User]:
        """Read user by ID"""
        pass