from abc import ABC, abstractmethod
from typing import Any

from app.models.user import User


class Permission(ABC):
    """Abstract base class for permission checking."""

    @abstractmethod
    async def authorize(self, user: User, resource: Any = None) -> bool:
        """Check if user has permission to access the resource.

        Args:
            user: The user to check permissions for
            resource: Optional resource being accessed

        Returns:
            True if user has permission, False otherwise
        """
        pass
