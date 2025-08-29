"""
Tests for register request schema.
"""

import unittest
from datetime import datetime

from pydantic import ValidationError

from app.schemas.register_request import RegisterRequest


class TestRegisterRequestSchema(unittest.TestCase):
    """Test cases for register request schema."""

    def test_valid_register_request(self):
        """Test creating a valid register request."""
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",  # Valid password with all requirements
            "first_name": "John",
            "last_name": "Doe",
            "dob": datetime(1990, 1, 1),
        }

        # Act
        request = RegisterRequest(**request_data)

        # Assert
        self.assertEqual(request.email, "test@example.com")
        self.assertEqual(request.password, "TestPassword123!")
        self.assertEqual(request.first_name, "John")
        self.assertEqual(request.last_name, "Doe")
        self.assertEqual(request.dob, datetime(1990, 1, 1))

    def test_register_request_serialization(self):
        """Test that RegisterRequest can be serialized to dict."""
        # Arrange
        request_data = {
            "email": "test@example.com",
            "password": "Password123!",  # Valid password with all requirements
            "first_name": "Jane",
            "last_name": "Smith",
            "dob": datetime(1995, 6, 15),
        }
        request = RegisterRequest(**request_data)

        # Act
        serialized = request.model_dump()

        # Assert
        self.assertEqual(serialized["email"], "test@example.com")
        self.assertEqual(serialized["password"], "Password123!")
        self.assertEqual(serialized["first_name"], "Jane")
        self.assertEqual(serialized["last_name"], "Smith")
        self.assertEqual(serialized["dob"], datetime(1995, 6, 15))

    def test_missing_required_fields(self):
        """Test that missing required fields raise validation error."""
        # Act & Assert
        with self.assertRaises(ValidationError):
            RegisterRequest(email="test@example.com")

    def test_invalid_email_format(self):
        """Test that invalid email format raises validation error."""
        # Arrange
        request_data = {
            "email": "invalid-email",
            "password": "Password123!",  # Valid password
            "first_name": "John",
            "last_name": "Doe",
            "dob": datetime(1990, 1, 1),
        }

        # Act & Assert
        # Should raise validation error for invalid email format
        with self.assertRaises(ValidationError):
            RegisterRequest(**request_data)


if __name__ == "__main__":
    unittest.main()
