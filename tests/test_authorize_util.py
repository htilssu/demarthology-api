"""
Tests for authorization utilities.
"""

import unittest
from typing import Any
from unittest.mock import MagicMock

from fastapi import HTTPException

from app.models.user import User
from app.utils.authorize import BasicContext, Permission, PermissionContext, authorize


class MockPermissionContext(PermissionContext[Any]):
    """Mock permission context for testing."""

    def __init__(self, user: User | None = None, obj: Any = None):
        self.user = user
        self.obj = obj

    def get_user(self) -> User | None:
        return self.user

    def get_obj(self) -> Any:
        return self.obj


class MockPermission(Permission[Any]):
    """Mock permission for testing."""

    def __init__(self, should_authorize: bool = True):
        self.should_authorize = should_authorize

    async def authorize(self, context: PermissionContext[Any]) -> bool:
        return self.should_authorize


class TestAuthorizeUtil(unittest.IsolatedAsyncioTestCase):
    """Test cases for authorization utility."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = MagicMock(spec=User)
        self.user.id = "user123"
        self.user.email = "test@example.com"
        self.user.role = "user"

        self.context = MockPermissionContext(user=self.user)

    async def test_authorize_allows_access(self):
        """Test authorize passes when permission allows."""
        # Arrange
        permission = MockPermission(should_authorize=True)

        # Act & Assert (should not raise exception)
        await authorize(permission, self.context)

    async def test_authorize_denies_access(self):
        """Test authorize raises HTTPException when permission denies."""
        # Arrange
        permission = MockPermission(should_authorize=False)

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await authorize(permission, self.context)

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(context.exception.detail, "Insufficient permissions")

    async def test_authorize_with_resource_context(self):
        """Test authorize works with resource in context."""
        # Arrange
        permission = MockPermission(should_authorize=True)
        context_with_resource = MockPermissionContext(user=self.user, obj={"id": "resource123"})

        # Act & Assert (should not raise exception)
        await authorize(permission, context_with_resource)

    async def test_basic_context_creation(self):
        """Test BasicContext can be created and used."""
        # Arrange
        basic_context = BasicContext(user=self.user, obj={"test": "data"})
        permission = MockPermission(should_authorize=True)

        # Act & Assert
        await authorize(permission, basic_context)
        self.assertEqual(basic_context.get_user(), self.user)
        self.assertEqual(basic_context.get_obj(), {"test": "data"})


if __name__ == "__main__":
    unittest.main()
