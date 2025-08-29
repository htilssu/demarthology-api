"""
Tests for authorization utilities.
"""

import unittest
from unittest.mock import MagicMock

from fastapi import HTTPException

from app.models.user import User
from app.utils.authorize import (
    check_all_permissions,
    check_any_permission,
    check_permission,
    require_all_permissions,
    require_any_permission,
    require_permission,
)
from app.utils.permission import Permission


class MockPermission(Permission):
    """Mock permission for testing."""

    def __init__(self, should_authorize: bool = True):
        self.should_authorize = should_authorize

    async def authorize(self, user: User, resource=None) -> bool:
        return self.should_authorize


class TestAuthorizeUtil(unittest.IsolatedAsyncioTestCase):
    """Test cases for authorization utility."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = MagicMock(spec=User)
        self.user.id = "user123"
        self.user.email = "test@example.com"
        self.user.role = "user"

    async def test_check_permission_allows_access(self):
        """Test check_permission returns True when permission allows."""
        # Arrange
        permission = MockPermission(should_authorize=True)

        # Act
        result = await check_permission(self.user, permission)

        # Assert
        self.assertTrue(result)

    async def test_check_permission_denies_access(self):
        """Test check_permission returns False when permission denies."""
        # Arrange
        permission = MockPermission(should_authorize=False)

        # Act
        result = await check_permission(self.user, permission)

        # Assert
        self.assertFalse(result)

    async def test_require_permission_allows_access(self):
        """Test require_permission passes when permission allows."""
        # Arrange
        permission = MockPermission(should_authorize=True)

        # Act & Assert (should not raise exception)
        await require_permission(self.user, permission)

    async def test_require_permission_denies_access(self):
        """Test require_permission raises HTTPException when permission denies."""
        # Arrange
        permission = MockPermission(should_authorize=False)

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await require_permission(self.user, permission)

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(context.exception.detail, "Insufficient permissions")

    async def test_check_any_permission_with_one_allowed(self):
        """Test check_any_permission returns True when at least one permission allows."""
        # Arrange
        permissions = [
            MockPermission(should_authorize=False),
            MockPermission(should_authorize=True),
            MockPermission(should_authorize=False),
        ]

        # Act
        result = await check_any_permission(self.user, permissions)

        # Assert
        self.assertTrue(result)

    async def test_check_any_permission_with_none_allowed(self):
        """Test check_any_permission returns False when no permissions allow."""
        # Arrange
        permissions = [
            MockPermission(should_authorize=False),
            MockPermission(should_authorize=False),
            MockPermission(should_authorize=False),
        ]

        # Act
        result = await check_any_permission(self.user, permissions)

        # Assert
        self.assertFalse(result)

    async def test_check_all_permissions_with_all_allowed(self):
        """Test check_all_permissions returns True when all permissions allow."""
        # Arrange
        permissions = [
            MockPermission(should_authorize=True),
            MockPermission(should_authorize=True),
            MockPermission(should_authorize=True),
        ]

        # Act
        result = await check_all_permissions(self.user, permissions)

        # Assert
        self.assertTrue(result)

    async def test_check_all_permissions_with_one_denied(self):
        """Test check_all_permissions returns False when any permission denies."""
        # Arrange
        permissions = [
            MockPermission(should_authorize=True),
            MockPermission(should_authorize=False),
            MockPermission(should_authorize=True),
        ]

        # Act
        result = await check_all_permissions(self.user, permissions)

        # Assert
        self.assertFalse(result)

    async def test_require_any_permission_allows_access(self):
        """Test require_any_permission passes when at least one permission allows."""
        # Arrange
        permissions = [
            MockPermission(should_authorize=False),
            MockPermission(should_authorize=True),
        ]

        # Act & Assert (should not raise exception)
        await require_any_permission(self.user, permissions)

    async def test_require_any_permission_denies_access(self):
        """Test require_any_permission raises HTTPException when no permissions allow."""
        # Arrange
        permissions = [
            MockPermission(should_authorize=False),
            MockPermission(should_authorize=False),
        ]

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await require_any_permission(self.user, permissions)

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(context.exception.detail, "Insufficient permissions")

    async def test_require_all_permissions_allows_access(self):
        """Test require_all_permissions passes when all permissions allow."""
        # Arrange
        permissions = [
            MockPermission(should_authorize=True),
            MockPermission(should_authorize=True),
        ]

        # Act & Assert (should not raise exception)
        await require_all_permissions(self.user, permissions)

    async def test_require_all_permissions_denies_access(self):
        """Test require_all_permissions raises HTTPException when any permission denies."""
        # Arrange
        permissions = [
            MockPermission(should_authorize=True),
            MockPermission(should_authorize=False),
        ]

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await require_all_permissions(self.user, permissions)

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(context.exception.detail, "Insufficient permissions")


if __name__ == "__main__":
    unittest.main()
