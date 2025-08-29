"""
Tests for login use case.
"""

import unittest
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException

from app.models.user import User
from app.services.user_service import UserService
from app.schemas.login_request import LoginRequest
from app.use_cases.login_uc import LoginUC
from app.utils.password import hash_password


class TestLoginUC(unittest.IsolatedAsyncioTestCase):
    """Test cases for login use case."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_user_service = AsyncMock(spec=UserService)
        self.login_uc = LoginUC(user_service=self.mock_user_service)

    async def test_successful_login(self):
        """Test successful login with correct credentials."""
        # Arrange
        test_password = "testpassword123"
        hashed_password = hash_password(test_password)

        mock_user = MagicMock(spec=User)
        mock_user.id = "user123"
        mock_user.email = "test@example.com"
        mock_user.password = hashed_password
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"

        self.mock_user_service.find_by_email.return_value = mock_user

        login_request = LoginRequest(email="test@example.com", password=test_password)

        # Act
        result = await self.login_uc.action(login_request)

        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Login successful")
        self.assertEqual(result.user.email, "test@example.com")
        self.assertEqual(result.user.first_name, "John")
        self.assertEqual(result.user.last_name, "Doe")
        self.assertEqual(result.user.role, "user")
        self.assertIsNotNone(result.access_token)
        self.assertEqual(result.token_type, "bearer")
        self.mock_user_service.find_by_email.assert_called_once_with("test@example.com")

    async def test_login_user_not_found(self):
        """Test login with non-existent user."""
        # Arrange
        self.mock_user_service.find_by_email.return_value = None

        login_request = LoginRequest(
            email="nonexistent@example.com", password="anypassword"
        )

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await self.login_uc.action(login_request)

        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid credentials")

    async def test_login_invalid_password(self):
        """Test login with incorrect password."""
        # Arrange
        correct_password = "correctpassword"
        wrong_password = "wrongpassword"
        hashed_password = hash_password(correct_password)

        mock_user = MagicMock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.password = hashed_password
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"

        self.mock_user_service.find_by_email.return_value = mock_user

        login_request = LoginRequest(email="test@example.com", password=wrong_password)

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await self.login_uc.action(login_request)

        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid credentials")


if __name__ == "__main__":
    unittest.main()
