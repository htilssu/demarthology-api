from abc import ABC, abstractmethod
from typing import Any, List
from fastapi import HTTPException, status

from app.models.user import User


class PermissionContext[T](ABC):
    """Abstract base class for permission contexts."""

    @abstractmethod
    def get_user(self) -> User | None:
        """Get the user from the context."""
        pass

    @abstractmethod
    def get_obj(self) -> T | None:
        """Get the object from the context."""
        pass


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


# Concrete Context Classes
class BasicContext(PermissionContext[Any]):
    """Basic permission context with user and optional object."""

    def __init__(self, user: User | None = None, obj: Any = None):
        self.user = user
        self.obj = obj

    def get_user(self) -> User | None:
        return self.user

    def get_obj(self) -> Any:
        return self.obj


class CanEditRoleContext(PermissionContext[User]):
    """Context for role editing permissions."""

    def __init__(self, user: User | None = None, obj: User | None = None):
        self.user = user
        self.obj = obj

    def get_user(self) -> User | None:
        return self.user

    def get_obj(self) -> User | None:
        return self.obj


class AdminOnlyContext(PermissionContext[Any]):
    """Context for admin-only permissions."""

    def __init__(self, user: User | None = None, obj: Any = None):
        self.user = user
        self.obj = obj

    def get_user(self) -> User | None:
        return self.user

    def get_obj(self) -> Any:
        return self.obj


class ResourceOwnerContext(PermissionContext[Any]):
    """Context for resource ownership permissions."""

    def __init__(self, user: User | None = None, obj: Any = None):
        self.user = user
        self.obj = obj

    def get_user(self) -> User | None:
        return self.user

    def get_obj(self) -> Any:
        return self.obj


# Concrete Permission Classes
class CanEditRole(Permission[User]):
    """Permission for editing user roles."""

    async def authorize(self, context: CanEditRoleContext) -> bool:
        """Check if user can edit roles.

        Args:
            context: Context containing user and target user

        Returns:
            True if user can edit roles, False otherwise
        """
        user = context.get_user()
        if not user:
            return False
        return user.role == "admin"


class AdminPermission(Permission[Any]):
    """Permission for admin users only."""

    async def authorize(self, context: AdminOnlyContext) -> bool:
        """Check if user is admin.

        Args:
            context: Permission context containing user

        Returns:
            True if user is admin, False otherwise
        """
        user = context.get_user()
        if not user:
            return False
        return user.role == "admin"


class UserPermission(Permission[Any]):
    """Permission for regular users and above."""

    async def authorize(self, context: BasicContext) -> bool:
        """Check if user has at least user role.

        Args:
            context: Permission context containing user

        Returns:
            True if user has user role or higher, False otherwise
        """
        user = context.get_user()
        if not user:
            return False
        return user.role in ["user", "admin", "moderator"]


class RolePermission(Permission[Any]):
    """Permission based on user role."""

    def __init__(self, required_role: str):
        """Initialize with required role.

        Args:
            required_role: The role required for permission
        """
        self.required_role = required_role

    async def authorize(self, context: BasicContext) -> bool:
        """Check if user has the required role.

        Args:
            context: Permission context containing user

        Returns:
            True if user has the required role, False otherwise
        """
        user = context.get_user()
        if not user:
            return False
        return user.role == self.required_role


class AnyRolePermission(Permission[Any]):
    """Permission based on having any of the specified roles."""

    def __init__(self, allowed_roles: List[str]):
        """Initialize with allowed roles.

        Args:
            allowed_roles: List of roles that grant permission
        """
        self.allowed_roles = allowed_roles

    async def authorize(self, context: BasicContext) -> bool:
        """Check if user has any of the allowed roles.

        Args:
            context: Permission context containing user

        Returns:
            True if user has any of the allowed roles, False otherwise
        """
        user = context.get_user()
        if not user:
            return False
        return user.role in self.allowed_roles


class SelfOrAdminPermission(Permission[Any]):
    """Permission for user to access own resources or admin to access any."""

    async def authorize(self, context: ResourceOwnerContext) -> bool:
        """Check if user can access the resource.

        Args:
            context: Permission context containing user and resource

        Returns:
            True if user is admin or owns the resource, False otherwise
        """
        user = context.get_user()
        if not user:
            return False

        # Admin can access everything
        if user.role == "admin":
            return True

        resource = context.get_obj()
        # If no resource specified, allow access
        if resource is None:
            return True

        # Check if user owns the resource
        if hasattr(resource, "user_id"):
            return str(resource.user_id) == str(user.id)
        elif hasattr(resource, "email"):
            return resource.email == user.email
        elif hasattr(resource, "owner_id"):
            return str(resource.owner_id) == str(user.id)

        # Default to deny if we can't determine ownership
        return False


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
