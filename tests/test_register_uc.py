"""
Tests for register use case.
"""

import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException

from app.models.user import User
from app.services.user_service import UserService
from app.schemas.register_request import RegisterRequest
from app.use_cases.register_uc import RegisterUC


class TestRegisterUC(unittest.IsolatedAsyncioTestCase):
    """Test cases for register use case."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_user_service = AsyncMock(spec=UserService)
        self.register_uc = RegisterUC(user_service=self.mock_user_service)

    async def test_successful_registration(self):
        """Test successful user registration."""
        # Arrange
        register_request = RegisterRequest(
            email="newuser@example.com",
            password="password123",
            confirm_password="password123",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user doesn't exist
        self.mock_user_service.check_user_exist.return_value = False

        # Mock the User creation and save_user method
        mock_user = MagicMock(spec=User)
        mock_user.email = "newuser@example.com"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        self.mock_user_service.save_user.return_value = mock_user

        with unittest.mock.patch(
            "app.use_cases.register_uc.User", return_value=mock_user
        ):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert
            self.assertTrue(result.success)
            self.assertEqual(result.message, "Registration successful")
            self.assertEqual(result.user.email, "newuser@example.com")
            self.assertEqual(result.user.first_name, "John")
            self.assertEqual(result.user.last_name, "Doe")
            self.mock_user_service.check_user_exist.assert_called_once_with(
                "newuser@example.com"
            )
            self.mock_user_service.save_user.assert_called_once_with(mock_user)

    async def test_registration_passwords_do_not_match(self):
        """Test registration fails when passwords don't match."""
        # Arrange
        register_request = RegisterRequest(
            email="newuser@example.com",
            password="password123",
            confirm_password="differentpassword",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await self.register_uc.action(register_request)

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Passwords do not match")

    async def test_registration_user_already_exists(self):
        """Test registration fails when user already exists."""
        # Arrange
        register_request = RegisterRequest(
            email="existing@example.com",
            password="password123",
            confirm_password="password123",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user already exists
        self.mock_user_service.check_user_exist.return_value = True

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await self.register_uc.action(register_request)

        self.assertEqual(context.exception.status_code, 409)
        self.assertEqual(
            context.exception.detail, "User with this email already exists"
        )

    async def test_password_is_hashed(self):
        """Test that password is properly hashed before saving."""
        # Arrange
        plain_password = "plainpassword123"
        register_request = RegisterRequest(
            email="test@example.com",
            password=plain_password,
            confirm_password=plain_password,
            first_name="Test",
            last_name="User",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user doesn't exist
        self.mock_user_service.check_user_exist.return_value = False

        # Mock the User creation and capture constructor arguments
        created_users = []

        def mock_user_init(*args, **kwargs):
            mock_user = MagicMock(spec=User)
            mock_user.email = kwargs.get("email")
            mock_user.first_name = kwargs.get("first_name")
            mock_user.last_name = kwargs.get("last_name")
            mock_user.password = kwargs.get("password")
            created_users.append(mock_user)
            return mock_user

        # Mock save_user to return the created user
        self.mock_user_service.save_user.side_effect = lambda user: user

        with unittest.mock.patch(
            "app.use_cases.register_uc.User", side_effect=mock_user_init
        ):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert
            self.assertTrue(result.success)
            self.assertEqual(len(created_users), 1)
            created_user = created_users[0]
            self.assertNotEqual(
                created_user.password, plain_password
            )  # Password should be hashed
            self.assertTrue(
                created_user.password.startswith("$2b$")
            )  # bcrypt hash format


if __name__ == "__main__":
    unittest.main()
