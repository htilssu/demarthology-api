from abc import ABC, abstractmethod
from typing import Any, List

from fastapi import HTTPException, status

from app.models.user import User


class PermissionContext(ABC):
    """Abstract base class for permission contexts."""
    
    def get_user(self) -> User | None:
        """Get the user from the context."""
        return getattr(self, 'user', None)
    
    def get_obj(self) -> Any:
        """Get the object from the context."""
        return getattr(self, 'obj', None)


class Permission(ABC):
    """Abstract base class for permission checking."""

    @abstractmethod
    async def authorize(self, context: PermissionContext) -> bool:
        """Check if permission is granted based on the context.

        Args:
            context: The permission context containing user and optional resource

        Returns:
            True if permission is granted, False otherwise
        """
        pass


class BasicContext(PermissionContext):
    """Basic permission context for common use cases."""

    def __init__(self, user: User | None = None, obj: Any = None):
        self.user = user
        self.obj = obj

    def get_user(self) -> User | None:
        return self.user

    def get_obj(self) -> Any:
        return self.obj


class AdminOnlyContext(PermissionContext):
    """Context for admin-only operations."""

    def __init__(self, user: User | None = None, obj: Any = None):
        self.user = user
        self.obj = obj

    def get_user(self) -> User | None:
        return self.user

    def get_obj(self) -> Any:
        return self.obj


class ResourceOwnerContext(PermissionContext):
    """Context for resource ownership permissions."""

    def __init__(self, user: User | None = None, obj: Any = None):
        self.user = user
        self.obj = obj

    def get_user(self) -> User | None:
        return self.user

    def get_obj(self) -> Any:
        return self.obj


class CanEditRoleContext(PermissionContext):
    """Context for role editing permissions."""

    def __init__(self, user: User | None = None, obj: User | None = None):
        self.user = user
        self.obj = obj

    def get_user(self) -> User | None:
        return self.user

    def get_obj(self) -> User | None:
        return self.obj


class RolePermission(Permission):
    """Permission that checks for a specific role."""

    def __init__(self, required_role: str):
        self.required_role = required_role

    async def authorize(self, context: PermissionContext) -> bool:
        user = context.get_user()
        if not user:
            return False
        return user.role == self.required_role


class AnyRolePermission(Permission):
    """Permission that checks for any of the specified roles."""

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def authorize(self, context: PermissionContext) -> bool:
        user = context.get_user()
        if not user:
            return False
        return user.role in self.allowed_roles


class AdminPermission(Permission):
    """Permission that allows only admin users."""

    async def authorize(self, context: PermissionContext) -> bool:
        user = context.get_user()
        if not user:
            return False
        return user.role == "admin"


class UserPermission(Permission):
    """Permission that allows authenticated users with valid roles."""

    VALID_ROLES = ["user", "admin", "moderator"]

    async def authorize(self, context: PermissionContext) -> bool:
        user = context.get_user()
        if not user:
            return False
        return user.role in self.VALID_ROLES


class SelfOrAdminPermission(Permission):
    """Permission that allows resource owners or admin users."""

    async def authorize(self, context: PermissionContext) -> bool:
        user = context.get_user()
        if not user:
            return False

        # Admin can access anything
        if user.role == "admin":
            return True

        # If no resource, allow (user can access their own data)
        obj = context.get_obj()
        if obj is None:
            return True

        # Check if user owns the resource
        if hasattr(obj, 'user_id') and str(obj.user_id) == str(user.id):
            return True
        if hasattr(obj, 'email') and str(obj.email) == str(user.email):
            return True
        if hasattr(obj, 'owner_id') and str(obj.owner_id) == str(user.id):
            return True

        return False


class CanEditRole(Permission):
    """Permission for editing user roles."""

    async def authorize(self, context: PermissionContext) -> bool:
        user = context.get_user()
        if not user:
            return False
        return user.role == "admin"


async def authorize(permission: Permission, context: PermissionContext) -> None:
    """Authorize access based on permission and context.

    Args:
        permission: The permission instance to check
        context: The permission context containing user and optional resource

    Raises:
        HTTPException: If permission is not granted (403 Forbidden)
    """
    if not await permission.authorize(context):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
