"""
Tests for register response schema.
"""

import unittest

from app.schemas.login_response import UserInfo
from app.schemas.register_response import RegisterResponse


class TestRegisterResponseSchema(unittest.TestCase):
    """Test cases for register response schema."""

    def test_register_response_creation(self):
        """Test RegisterResponse model creation."""
        # Arrange
        user_info = UserInfo(email="test@example.com", first_name="John", last_name="Doe", role="user")

        # Act
        response = RegisterResponse(
            success=True, 
            message="Registration successful", 
            user=user_info,
            access_token="sample_jwt_token"
        )

        # Assert
        self.assertTrue(response.success)
        self.assertEqual(response.message, "Registration successful")
        self.assertEqual(response.user.email, "test@example.com")
        self.assertEqual(response.user.first_name, "John")
        self.assertEqual(response.user.last_name, "Doe")
        self.assertEqual(response.user.role, "user")
        self.assertEqual(response.access_token, "sample_jwt_token")
        self.assertEqual(response.token_type, "bearer")

    def test_register_response_serialization(self):
        """Test that RegisterResponse can be serialized to JSON for middleware."""
        # Arrange
        user_info = UserInfo(email="jane@example.com", first_name="Jane", last_name="Smith", role="user")
        response = RegisterResponse(
            success=True, 
            message="User registered successfully", 
            user=user_info,
            access_token="example_jwt_token_12345"
        )

        # Act
        serialized = response.model_dump()

        # Assert
        expected = {
            "success": True,
            "message": "User registered successfully",
            "user": {
                "email": "jane@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "role": "user",
            },
            "access_token": "example_jwt_token_12345",
            "token_type": "bearer",
        }
        self.assertEqual(serialized, expected)


if __name__ == "__main__":
    unittest.main()
