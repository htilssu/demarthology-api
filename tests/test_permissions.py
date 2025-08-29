"""
Tests for concrete permission implementations.
"""

import unittest
from unittest.mock import MagicMock

from app.models.user import User
from app.utils.permissions import (
    AdminPermission,
    AnyRolePermission,
    RolePermission,
    SelfOrAdminPermission,
    UserPermission,
)


class TestRolePermission(unittest.IsolatedAsyncioTestCase):
    """Test cases for RolePermission."""

    async def test_authorize_with_matching_role(self):
        """Test authorization succeeds with matching role."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "admin"
        permission = RolePermission("admin")
        context = {"user": user}

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
        context = {"user": user}

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = RolePermission("admin")
        context = {}

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
        context = {"user": user}

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
        context = {"user": user}

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = AnyRolePermission(["admin", "moderator"])
        context = {}

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
        context = {"user": user}

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
        context = {"user": user}

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = AdminPermission()
        context = {}

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
        context = {"user": user}

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
        context = {"user": user}

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
        context = {"user": user}

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
        context = {"user": user}

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = UserPermission()
        context = {}

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
        context = {"user": user}

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
        context = {"user": user, "resource": None}

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
        context = {"user": user, "resource": resource}

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
        context = {"user": user, "resource": resource}

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
        context = {"user": user, "resource": resource}

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
        context = {"user": user, "resource": resource}

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
        context = {"user": user, "resource": resource}

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)

    async def test_authorize_with_no_user(self):
        """Test authorization fails with no user in context."""
        # Arrange
        permission = SelfOrAdminPermission()
        context = {}

        # Act
        result = await permission.authorize(context)

        # Assert
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
