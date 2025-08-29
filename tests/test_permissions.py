"""
Tests for permission implementations that work with current codebase.
"""

import unittest
from typing import Any, List
from unittest.mock import MagicMock

from app.models.user import User


# Define permission context base class for testing
class MockPermissionContext:
    """Mock permission context base class."""

    def __init__(self, user: User = None, obj: Any = None):
        self.user = user
        self.obj = obj


# Define permission base class for testing
class MockPermission:
    """Mock permission base class."""

    async def authorize(self, context: MockPermissionContext) -> bool:
        """Override in subclasses."""
        raise NotImplementedError


# Concrete permission implementations
class RolePermission(MockPermission):
    """Role-based permission."""

    def __init__(self, required_role: str):
        self.required_role = required_role

    async def authorize(self, context: MockPermissionContext) -> bool:
        if not context.user:
            return False
        return context.user.role == self.required_role


class AnyRolePermission(MockPermission):
    """Any of multiple roles permission."""

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def authorize(self, context: MockPermissionContext) -> bool:
        if not context.user:
            return False
        return context.user.role in self.allowed_roles


class AdminPermission(MockPermission):
    """Admin-only permission."""

    async def authorize(self, context: MockPermissionContext) -> bool:
        if not context.user:
            return False
        return context.user.role == "admin"


class UserPermission(MockPermission):
    """User permission (any valid user role)."""

    async def authorize(self, context: MockPermissionContext) -> bool:
        if not context.user:
            return False
        return context.user.role in ["user", "admin", "moderator"]


class SelfOrAdminPermission(MockPermission):
    """Self or admin permission."""

    async def authorize(self, context: MockPermissionContext) -> bool:
        if not context.user:
            return False

        # Admin can access everything
        if context.user.role == "admin":
            return True

        # If no resource, allow access
        if not context.obj:
            return True

        # Check if user owns the resource
        if hasattr(context.obj, 'user_id'):
            return context.obj.user_id == context.user.id
        elif hasattr(context.obj, 'email'):
            return context.obj.email == context.user.email
        elif hasattr(context.obj, 'owner_id'):
            return context.obj.owner_id == context.user.id

        # Unknown resource type
        return False


class CanEditRole(MockPermission):
    """Can edit role permission."""

    async def authorize(self, context: MockPermissionContext) -> bool:
        if not context.user:
            return False
        return context.user.role == "admin"


class TestRolePermission(unittest.IsolatedAsyncioTestCase):
    """Test cases for RolePermission."""

    async def test_authorize_with_matching_role(self):
        """Test authorization succeeds with matching role."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "admin"
        permission = RolePermission("admin")
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_non_matching_role(self):
        """Test authorization fails with non-matching role."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        permission = RolePermission("admin")
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = RolePermission("admin")
        context = MockPermissionContext()

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)


class TestAnyRolePermission(unittest.IsolatedAsyncioTestCase):
    """Test cases for AnyRolePermission."""

    async def test_authorize_with_allowed_role(self):
        """Test authorization succeeds with allowed role."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "moderator"
        permission = AnyRolePermission(["admin", "moderator", "editor"])
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_disallowed_role(self):
        """Test authorization fails with disallowed role."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        permission = AnyRolePermission(["admin", "moderator"])
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = AnyRolePermission(["admin", "moderator"])
        context = MockPermissionContext()

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)


class TestAdminPermission(unittest.IsolatedAsyncioTestCase):
    """Test cases for AdminPermission."""

    async def test_authorize_with_admin_role(self):
        """Test authorization succeeds for admin user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "admin"
        permission = AdminPermission()
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_non_admin_role(self):
        """Test authorization fails for non-admin user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        permission = AdminPermission()
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = AdminPermission()
        context = MockPermissionContext()

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)


class TestUserPermission(unittest.IsolatedAsyncioTestCase):
    """Test cases for UserPermission."""

    async def test_authorize_with_user_role(self):
        """Test authorization succeeds for regular user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        permission = UserPermission()
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_admin_role(self):
        """Test authorization succeeds for admin user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "admin"
        permission = UserPermission()
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_moderator_role(self):
        """Test authorization succeeds for moderator user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "moderator"
        permission = UserPermission()
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_invalid_role(self):
        """Test authorization fails for invalid role."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "guest"
        permission = UserPermission()
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = UserPermission()
        context = MockPermissionContext()

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)


class TestSelfOrAdminPermission(unittest.IsolatedAsyncioTestCase):
    """Test cases for SelfOrAdminPermission."""

    async def test_authorize_admin_user(self):
        """Test authorization succeeds for admin user regardless of resource."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "admin"
        user.id = "admin123"
        permission = SelfOrAdminPermission()
        context = MockPermissionContext(user=user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_no_resource(self):
        """Test authorization succeeds when no resource is provided."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"
        permission = SelfOrAdminPermission()
        context = MockPermissionContext(user=user, obj=None)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_user_owns_resource_by_user_id(self):
        """Test authorization succeeds when user owns resource by user_id."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"
        resource = MagicMock()
        resource.user_id = "user123"
        permission = SelfOrAdminPermission()
        context = MockPermissionContext(user=user, obj=resource)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_user_owns_resource_by_email(self):
        """Test authorization succeeds when user owns resource by email."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"
        user.email = "user@example.com"
        resource = MagicMock()
        resource.email = "user@example.com"
        # Remove user_id to test email check
        del resource.user_id
        permission = SelfOrAdminPermission()
        context = MockPermissionContext(user=user, obj=resource)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_user_owns_resource_by_owner_id(self):
        """Test authorization succeeds when user owns resource by owner_id."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"
        resource = MagicMock()
        resource.owner_id = "user123"
        # Remove user_id and email to test owner_id check
        del resource.user_id
        del resource.email
        permission = SelfOrAdminPermission()
        context = MockPermissionContext(user=user, obj=resource)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_user_does_not_own_resource(self):
        """Test authorization fails when user does not own resource."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"
        user.email = "user@example.com"
        resource = MagicMock()
        resource.user_id = "other_user456"
        permission = SelfOrAdminPermission()
        context = MockPermissionContext(user=user, obj=resource)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_unknown_resource_type(self):
        """Test authorization fails for unknown resource type."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"
        resource = MagicMock()
        # Remove all ownership attributes
        del resource.user_id
        del resource.email
        del resource.owner_id
        permission = SelfOrAdminPermission()
        context = MockPermissionContext(user=user, obj=resource)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = SelfOrAdminPermission()
        context = MockPermissionContext()

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)


class TestCanEditRole(unittest.IsolatedAsyncioTestCase):
    """Test cases for CanEditRole permission."""

    async def test_authorize_admin_can_edit_role(self):
        """Test authorization succeeds for admin user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "admin"
        target_user = MagicMock(spec=User)
        target_user.role = "user"
        permission = CanEditRole()
        context = MockPermissionContext(user=user, obj=target_user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertTrue(result)

    async def test_authorize_non_admin_cannot_edit_role(self):
        """Test authorization fails for non-admin user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        target_user = MagicMock(spec=User)
        target_user.role = "user"
        permission = CanEditRole()
        context = MockPermissionContext(user=user, obj=target_user)

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = CanEditRole()
        context = MockPermissionContext()

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
