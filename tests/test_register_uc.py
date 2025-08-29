"""
Tests for register use case.
"""

import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException
from pydantic import ValidationError

from app.models.user import User
from app.schemas.register_request import RegisterRequest
from app.services.user_service import UserService
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
            password="Password123!",  # Valid password with all requirements
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
        mock_user.role = "user"
        self.mock_user_service.save_user.return_value = mock_user

        with unittest.mock.patch("app.use_cases.register_uc.User", return_value=mock_user):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert
            self.assertTrue(result.success)
            self.assertEqual(result.message, "Registration successful")
            self.assertEqual(result.user.email, "newuser@example.com")
            self.assertEqual(result.user.first_name, "John")
            self.assertEqual(result.user.last_name, "Doe")
            self.assertEqual(result.user.role, "user")
            self.mock_user_service.check_user_exist.assert_called_once_with("newuser@example.com")
            self.mock_user_service.save_user.assert_called_once_with(mock_user)

    async def test_registration_user_already_exists(self):
        """Test registration fails when user already exists."""
        # Arrange
        register_request = RegisterRequest(
            email="existing@example.com",
            password="Password123!",  # Valid password with all requirements
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
        self.assertEqual(context.exception.detail, "User with this email already exists")

    async def test_password_is_hashed(self):
        """Test that password is properly hashed before saving."""
        # Arrange
        plain_password = "PlainPassword123!"  # Valid password with all requirements
        register_request = RegisterRequest(
            email="test@example.com",
            password=plain_password,
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
            mock_user.role = kwargs.get("role", "user")
            created_users.append(mock_user)
            return mock_user

        # Mock save_user to return the created user
        self.mock_user_service.save_user.side_effect = lambda user: user

        with unittest.mock.patch("app.use_cases.register_uc.User", side_effect=mock_user_init):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert
            self.assertTrue(result.success)
            self.assertEqual(len(created_users), 1)
            created_user = created_users[0]
            self.assertNotEqual(created_user.password, plain_password)  # Password should be hashed
            self.assertTrue(created_user.password.startswith("$2b$"))  # bcrypt hash format

    async def test_default_role_assignment(self):
        """Test that new users are assigned default 'user' role."""
        # Arrange
        register_request = RegisterRequest(
            email="newuser@example.com",
            password="Password123!",
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
        mock_user.role = "user"
        self.mock_user_service.save_user.return_value = mock_user

        with unittest.mock.patch("app.use_cases.register_uc.User", return_value=mock_user):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert
            self.assertEqual(result.user.role, "user")

    async def test_service_error_handling(self):
        """Test handling of service layer errors during registration."""
        # Arrange
        register_request = RegisterRequest(
            email="newuser@example.com",
            password="Password123!",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user doesn't exist
        self.mock_user_service.check_user_exist.return_value = False

        # Mock save_user to raise an exception
        self.mock_user_service.save_user.side_effect = Exception("Database error")

        mock_user = MagicMock(spec=User)
        with unittest.mock.patch("app.use_cases.register_uc.User", return_value=mock_user):
            # Act & Assert
            with self.assertRaises(Exception) as context:
                await self.register_uc.action(register_request)

            self.assertEqual(str(context.exception), "Database error")

    async def test_email_normalization(self):
        """Test that email addresses are properly handled."""
        # Arrange
        register_request = RegisterRequest(
            email="User@Example.COM",  # Mixed case email
            password="Password123!",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user doesn't exist
        self.mock_user_service.check_user_exist.return_value = False

        # Mock the User creation and save_user method
        mock_user = MagicMock(spec=User)
        mock_user.email = "User@example.com"  # Pydantic normalizes domain to lowercase
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"
        self.mock_user_service.save_user.return_value = mock_user

        with unittest.mock.patch("app.use_cases.register_uc.User", return_value=mock_user):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert
            self.assertTrue(result.success)
            # Email domain should be normalized to lowercase by pydantic EmailStr
            self.mock_user_service.check_user_exist.assert_called_once_with("User@example.com")


class TestRegisterRequestValidation(unittest.TestCase):
    """Test cases for RegisterRequest validation."""

    def test_valid_password_requirements(self):
        """Test that valid passwords are accepted."""
        valid_passwords = [
            "Password123!",
            "MySecure$Pass1",
            "Test123@Valid",
            "Complex!Password9",
        ]
        
        for password in valid_passwords:
            with self.subTest(password=password):
                # Should not raise validation error
                request = RegisterRequest(
                    email="test@example.com",
                    password=password,
                    first_name="Test",
                    last_name="User",
                    dob=datetime(1990, 1, 1),
                )
                self.assertEqual(request.password, password)

    def test_invalid_password_too_short(self):
        """Test that passwords shorter than 7 characters are rejected."""
        with self.assertRaises(ValidationError) as context:
            RegisterRequest(
                email="test@example.com",
                password="Pass1!",  # Only 6 characters
                first_name="Test",
                last_name="User",
                dob=datetime(1990, 1, 1),
            )
        
        self.assertIn("Password must be at least 7 characters long", str(context.exception))

    def test_invalid_password_no_uppercase(self):
        """Test that passwords without uppercase letters are rejected."""
        with self.assertRaises(ValidationError) as context:
            RegisterRequest(
                email="test@example.com",
                password="password123!",  # No uppercase
                first_name="Test",
                last_name="User",
                dob=datetime(1990, 1, 1),
            )
        
        self.assertIn("Password must contain at least one uppercase letter", str(context.exception))

    def test_invalid_password_no_lowercase(self):
        """Test that passwords without lowercase letters are rejected."""
        with self.assertRaises(ValidationError) as context:
            RegisterRequest(
                email="test@example.com",
                password="PASSWORD123!",  # No lowercase
                first_name="Test",
                last_name="User",
                dob=datetime(1990, 1, 1),
            )
        
        self.assertIn("Password must contain at least one lowercase letter", str(context.exception))

    def test_invalid_password_no_number(self):
        """Test that passwords without numbers are rejected."""
        with self.assertRaises(ValidationError) as context:
            RegisterRequest(
                email="test@example.com",
                password="Password!",  # No number
                first_name="Test",
                last_name="User",
                dob=datetime(1990, 1, 1),
            )
        
        self.assertIn("Password must contain at least one number", str(context.exception))

    def test_invalid_password_no_special_character(self):
        """Test that passwords without special characters are rejected."""
        with self.assertRaises(ValidationError) as context:
            RegisterRequest(
                email="test@example.com",
                password="Password123",  # No special character
                first_name="Test",
                last_name="User",
                dob=datetime(1990, 1, 1),
            )
        
        self.assertIn("Password must contain at least one special character", str(context.exception))

    def test_invalid_email_format(self):
        """Test that invalid email formats are rejected."""
        invalid_emails = [
            "notanemail",
            "invalid@",
            "@invalid.com",
            "spaces @example.com",
            "multiple@@example.com",
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                with self.assertRaises(ValidationError):
                    RegisterRequest(
                        email=email,
                        password="Password123!",
                        first_name="Test",
                        last_name="User",
                        dob=datetime(1990, 1, 1),
                    )

    def test_invalid_age_too_young(self):
        """Test that users under 13 years old are rejected."""
        # User who would be 12 years old
        too_young_dob = datetime.now().replace(year=datetime.now().year - 12)
        
        with self.assertRaises(ValidationError) as context:
            RegisterRequest(
                email="test@example.com",
                password="Password123!",
                first_name="Test",
                last_name="User",
                dob=too_young_dob,
            )
        
        self.assertIn("User must be at least 13 years old", str(context.exception))

    def test_invalid_future_birth_date(self):
        """Test that future birth dates are rejected."""
        # Birth date in the future
        future_dob = datetime.now().replace(year=datetime.now().year + 1)
        
        with self.assertRaises(ValidationError) as context:
            RegisterRequest(
                email="test@example.com",
                password="Password123!",
                first_name="Test",
                last_name="User",
                dob=future_dob,
            )
        
        self.assertIn("Date of birth cannot be in the future", str(context.exception))

    def test_valid_age_boundary(self):
        """Test that users exactly 13 years old are accepted."""
        # User who is exactly 13 years old
        thirteen_years_ago = datetime.now().replace(year=datetime.now().year - 13)
        
        # Should not raise validation error
        request = RegisterRequest(
            email="test@example.com",
            password="Password123!",
            first_name="Test",
            last_name="User",
            dob=thirteen_years_ago,
        )
        self.assertEqual(request.dob, thirteen_years_ago)


if __name__ == "__main__":
    unittest.main()
