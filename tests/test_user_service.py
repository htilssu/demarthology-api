"""
Tests for user service.
"""

import unittest
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


class TestUserService(unittest.IsolatedAsyncioTestCase):
    """Test cases for user service."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_user_repository = AsyncMock(spec=UserRepository)
        self.user_service = UserService(user_repository=self.mock_user_repository)

    async def test_check_user_exist_returns_true_when_user_exists(self):
        """Test check_user_exist returns True when user exists."""
        # Arrange
        mock_user = MagicMock(spec=User)
        self.mock_user_repository.find_by_email.return_value = mock_user

        # Act
        result = await self.user_service.check_user_exist("test@example.com")

        # Assert
        self.assertTrue(result)
        self.mock_user_repository.find_by_email.assert_called_once_with(
            "test@example.com"
        )

    async def test_check_user_exist_returns_false_when_user_not_exists(self):
        """Test check_user_exist returns False when user doesn't exist."""
        # Arrange
        self.mock_user_repository.find_by_email.return_value = None

        # Act
        result = await self.user_service.check_user_exist("test@example.com")

        # Assert
        self.assertFalse(result)
        self.mock_user_repository.find_by_email.assert_called_once_with(
            "test@example.com"
        )

    async def test_check_user_exist_handles_exception(self):
        """Test check_user_exist handles repository exceptions."""
        # Arrange
        self.mock_user_repository.find_by_email.side_effect = Exception(
            "Database error"
        )

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await self.user_service.check_user_exist("test@example.com")

        self.assertEqual(context.exception.status_code, 500)
        self.assertIn("Error checking user existence", context.exception.detail)

    async def test_save_user_success(self):
        """Test save_user successfully saves a user."""
        # Arrange
        mock_user = MagicMock(spec=User)
        mock_user.create = AsyncMock()

        # Act
        result = await self.user_service.save_user(mock_user)

        # Assert
        self.assertEqual(result, mock_user)
        mock_user.create.assert_called_once()

    async def test_save_user_handles_exception(self):
        """Test save_user handles exceptions during user creation."""
        # Arrange
        mock_user = MagicMock(spec=User)
        mock_user.create = AsyncMock(side_effect=Exception("Database error"))

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await self.user_service.save_user(mock_user)

        self.assertEqual(context.exception.status_code, 500)
        self.assertIn("Error saving user", context.exception.detail)

    async def test_find_by_email_success(self):
        """Test find_by_email successfully finds a user."""
        # Arrange
        mock_user = MagicMock(spec=User)
        self.mock_user_repository.find_by_email.return_value = mock_user

        # Act
        result = await self.user_service.find_by_email("test@example.com")

        # Assert
        self.assertEqual(result, mock_user)
        self.mock_user_repository.find_by_email.assert_called_once_with(
            "test@example.com"
        )

    async def test_find_by_email_handles_exception(self):
        """Test find_by_email handles repository exceptions."""
        # Arrange
        self.mock_user_repository.find_by_email.side_effect = Exception(
            "Database error"
        )

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await self.user_service.find_by_email("test@example.com")

        self.assertEqual(context.exception.status_code, 500)
        self.assertIn("Error finding user", context.exception.detail)


if __name__ == "__main__":
    unittest.main()
