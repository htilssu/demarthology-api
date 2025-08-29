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

        # Act
        result = await permission.authorize(user)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_non_matching_role(self):
        """Test authorization fails with non-matching role."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        permission = RolePermission("admin")

        # Act
        result = await permission.authorize(user)

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

        # Act
        result = await permission.authorize(user)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_disallowed_role(self):
        """Test authorization fails with disallowed role."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        permission = AnyRolePermission(["admin", "moderator"])

        # Act
        result = await permission.authorize(user)

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

        # Act
        result = await permission.authorize(user)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_non_admin_role(self):
        """Test authorization fails for non-admin user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        permission = AdminPermission()

        # Act
        result = await permission.authorize(user)

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

        # Act
        result = await permission.authorize(user)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_admin_role(self):
        """Test authorization succeeds for admin user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "admin"
        permission = UserPermission()

        # Act
        result = await permission.authorize(user)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_moderator_role(self):
        """Test authorization succeeds for moderator user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "moderator"
        permission = UserPermission()

        # Act
        result = await permission.authorize(user)

        # Assert
        self.assertTrue(result)

    async def test_authorize_with_invalid_role(self):
        """Test authorization fails for invalid role."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "guest"
        permission = UserPermission()

        # Act
        result = await permission.authorize(user)

        # Assert
        self.assertFalse(result)


class TestSelfOrAdminPermission(unittest.IsolatedAsyncioTestCase):
    """Test cases for SelfOrAdminPermission."""

    async def test_authorize_admin_user(self):
        """Test authorization succeeds for admin user."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "admin"
        user.id = "user123"
        permission = SelfOrAdminPermission()

        # Act
        result = await permission.authorize(user)

        # Assert
        self.assertTrue(result)

    async def test_authorize_no_resource(self):
        """Test authorization succeeds when no resource is specified."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"
        permission = SelfOrAdminPermission()

        # Act
        result = await permission.authorize(user, resource=None)

        # Assert
        self.assertTrue(result)

    async def test_authorize_user_owns_resource_by_user_id(self):
        """Test authorization succeeds when user owns resource (user_id)."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"

        resource = MagicMock()
        resource.user_id = "user123"

        permission = SelfOrAdminPermission()

        # Act
        result = await permission.authorize(user, resource)

        # Assert
        self.assertTrue(result)

    async def test_authorize_user_owns_resource_by_email(self):
        """Test authorization succeeds when user owns resource (email)."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"
        user.email = "test@example.com"

        # Create resource that only has email, not user_id
        resource = type("Resource", (), {"email": "test@example.com"})()

        permission = SelfOrAdminPermission()

        # Act
        result = await permission.authorize(user, resource)

        # Assert
        self.assertTrue(result)

    async def test_authorize_user_owns_resource_by_owner_id(self):
        """Test authorization succeeds when user owns resource (owner_id)."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"

        # Create resource that only has owner_id, not user_id or email
        resource = type("Resource", (), {"owner_id": "user123"})()

        permission = SelfOrAdminPermission()

        # Act
        result = await permission.authorize(user, resource)

        # Assert
        self.assertTrue(result)

    async def test_authorize_user_does_not_own_resource(self):
        """Test authorization fails when user doesn't own resource."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"
        user.email = "test@example.com"

        resource = MagicMock()
        resource.user_id = "otheruser456"

        permission = SelfOrAdminPermission()

        # Act
        result = await permission.authorize(user, resource)

        # Assert
        self.assertFalse(result)

    async def test_authorize_unknown_resource_type(self):
        """Test authorization fails for unknown resource type."""
        # Arrange
        user = MagicMock(spec=User)
        user.role = "user"
        user.id = "user123"

        # Create resource with no ownership attributes
        resource = type("Resource", (), {})()

        permission = SelfOrAdminPermission()

        # Act
        result = await permission.authorize(user, resource)

        # Assert
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
