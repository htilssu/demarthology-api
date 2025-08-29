"""
Tests for login response schema.
"""

import json
import unittest

from app.schemas.login_response import LoginResponse, UserInfo


class TestLoginResponseSchema(unittest.TestCase):
    """Test cases for login response schema."""

    def test_user_info_creation(self):
        """Test UserInfo model creation."""
        user_info = UserInfo(
            email="test@example.com", first_name="John", last_name="Doe"
        )

        self.assertEqual(user_info.email, "test@example.com")
        self.assertEqual(user_info.first_name, "John")
        self.assertEqual(user_info.last_name, "Doe")

    def test_login_response_creation(self):
        """Test LoginResponse model creation."""
        user_info = UserInfo(
            email="test@example.com", first_name="John", last_name="Doe"
        )
        response = LoginResponse(
            success=True,
            message="Login successful",
            user=user_info,
            access_token="test_token",
        )

        self.assertTrue(response.success)
        self.assertEqual(response.message, "Login successful")
        self.assertEqual(response.user.email, "test@example.com")
        self.assertEqual(response.user.first_name, "John")
        self.assertEqual(response.user.last_name, "Doe")
        self.assertEqual(response.access_token, "test_token")
        self.assertEqual(response.token_type, "bearer")

    def test_login_response_serialization(self):
        """Test that LoginResponse can be serialized to JSON for middleware."""
        user_info = UserInfo(
            email="test@example.com", first_name="John", last_name="Doe"
        )
        response = LoginResponse(
            success=True,
            message="Login successful",
            user=user_info,
            access_token="test_token",
        )

        # Test serialization to dict (what Pydantic provides for JSON)
        response_dict = response.model_dump()

        expected_dict = {
            "success": True,
            "message": "Login successful",
            "user": {
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
            },
            "access_token": "test_token",
            "token_type": "bearer",
        }

        self.assertEqual(response_dict, expected_dict)

        # Test JSON serialization
        json_str = json.dumps(response_dict)
        parsed_back = json.loads(json_str)
        self.assertEqual(parsed_back, expected_dict)


if __name__ == "__main__":
    unittest.main()
