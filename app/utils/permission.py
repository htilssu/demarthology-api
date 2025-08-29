from abc import ABC, abstractmethod
from typing import Any

from app.models.user import User

# Python 3.12 generic syntax for PermissionContext
type PermissionContext[T] = dict[str, T]


class Permission[T](ABC):
    """Abstract base class for permission checking."""

    @abstractmethod
    async def authorize(self, context: PermissionContext[T]) -> bool:
        """Check if permission is granted based on the context.

        Args:
            context: The permission context containing user and optional resource

        Returns:
            True if permission is granted, False otherwise
        """
        pass
