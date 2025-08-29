from typing import Optional
from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.domain.entities.user import User
from app.repositories.user_repository import UserRepository


class MongoUserCommandGateway(UserCommandGateway):
    """MongoDB implementation of UserCommandGateway"""
    
    def __init__(self):
        self._repository = UserRepository()
        self._repository.document_class = User
    
    async def read_by_id(self, user_id: str) -> Optional[User]:
        """Read user by ID"""
        try:
            user = await self._repository.get(user_id)
            return user
        except Exception:
            return None