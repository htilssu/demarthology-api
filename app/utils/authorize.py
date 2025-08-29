from abc import ABC, abstractmethod
from typing import Any, List
from fastapi import HTTPException, status

from app.models.user import User


class PermissionContext(ABC):
    pass


class Permission[PC: PermissionContext](ABC):
    """Abstract base class for permission checking."""

    @abstractmethod
    async def authorize(self, context: PC) -> bool:
        """Check if permission is granted based on the context.

        Args:
            context: The permission context containing user and optional resource

        Returns:
            True if permission is granted, False otherwise
        """
        pass


class CanEditRoleContext(PermissionContext[User]):
    """Context for role editing permissions."""

    def __init__(self, user: User | None = None, obj: User | None = None):
        self.user = user
        self.obj = obj

    def get_user(self) -> User | None:
        return self.user

    def get_obj(self) -> User | None:
        return self.obj


async def authorize[T](
        permission: Permission[T], context: PermissionContext[T]
) -> None:
    """Authorize access based on permission and context.

    Args:
        permission: The permission instance to check
        context: The permission context containing user and optional resource

    Raises:
        HTTPException: If permission is not granted (403 Forbidden)
    """
    if not await permission.authorize(context):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )
