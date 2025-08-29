from abc import ABC, abstractmethod


class IdentityProvider(ABC):
    """Port for providing identity information"""
    
    @abstractmethod
    async def get_current_user_id(self) -> str:
        """Get the current user ID from the authentication context"""
        pass