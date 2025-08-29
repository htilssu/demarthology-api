from typing import Any, List

from app.models.user import User
from app.utils.permission import Permission


class RolePermission(Permission):
    """Permission based on user role."""

    def __init__(self, required_role: str):
        """Initialize with required role.

        Args:
            required_role: The role required for permission
        """
        self.required_role = required_role

    async def authorize(self, user: User, resource: Any = None) -> bool:
        """Check if user has the required role.

        Args:
            user: The user to check permissions for
            resource: Optional resource being accessed (not used)

        Returns:
            True if user has the required role, False otherwise
        """
        return user.role == self.required_role


class AnyRolePermission(Permission):
    """Permission based on having any of the specified roles."""

    def __init__(self, allowed_roles: List[str]):
        """Initialize with allowed roles.

        Args:
            allowed_roles: List of roles that grant permission
        """
        self.allowed_roles = allowed_roles

    async def authorize(self, user: User, resource: Any = None) -> bool:
        """Check if user has any of the allowed roles.

        Args:
            user: The user to check permissions for
            resource: Optional resource being accessed (not used)

        Returns:
            True if user has any of the allowed roles, False otherwise
        """
        return user.role in self.allowed_roles


class AdminPermission(Permission):
    """Permission for admin users only."""

    async def authorize(self, user: User, resource: Any = None) -> bool:
        """Check if user is admin.

        Args:
            user: The user to check permissions for
            resource: Optional resource being accessed (not used)

        Returns:
            True if user is admin, False otherwise
        """
        return user.role == "admin"


class UserPermission(Permission):
    """Permission for regular users and above."""

    async def authorize(self, user: User, resource: Any = None) -> bool:
        """Check if user has at least user role.

        Args:
            user: The user to check permissions for
            resource: Optional resource being accessed (not used)

        Returns:
            True if user has user role or higher, False otherwise
        """
        return user.role in ["user", "admin", "moderator"]


class SelfOrAdminPermission(Permission):
    """Permission for user to access own resources or admin to access any."""

    async def authorize(self, user: User, resource: Any = None) -> bool:
        """Check if user can access the resource.

        Args:
            user: The user to check permissions for
            resource: Resource being accessed (expected to have user_id or email)

        Returns:
            True if user is admin or owns the resource, False otherwise
        """
        # Admin can access everything
        if user.role == "admin":
            return True

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
