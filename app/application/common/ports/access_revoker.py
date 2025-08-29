from abc import ABC, abstractmethod


class AccessRevoker(ABC):
    """Port for revoking user access"""
    
    @abstractmethod
    async def remove_all_user_access(self, user_id: str) -> None:
        """Remove all access for a user"""
        pass