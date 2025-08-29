"""
Tests for UnauthorizedException.
"""

import unittest

from app.errors.unauthorized import UnauthorizedException


class TestUnauthorizedException(unittest.TestCase):
    """Test cases for UnauthorizedException."""

    def test_default_message(self):
        """Test UnauthorizedException with default message."""
        exception = UnauthorizedException()

        self.assertEqual(exception.message, "Unauthorized")
        self.assertIsNone(exception.detail)

    def test_custom_message(self):
        """Test UnauthorizedException with custom message."""
        custom_message = "Access denied"
        exception = UnauthorizedException(custom_message)

        self.assertEqual(exception.message, custom_message)
        self.assertIsNone(exception.detail)

    def test_with_detail(self):
        """Test UnauthorizedException with message and detail."""
        message = "Token expired"
        detail = "Please login again"
        exception = UnauthorizedException(message, detail)

        self.assertEqual(exception.message, message)
        self.assertEqual(exception.detail, detail)

    def test_inheritance(self):
        """Test that UnauthorizedException inherits from Exception."""
        exception = UnauthorizedException()

        self.assertIsInstance(exception, Exception)

    def test_str_representation(self):
        """Test string representation of the exception."""
        message = "Custom error message"
        exception = UnauthorizedException(message)

        self.assertEqual(str(exception), message)


if __name__ == "__main__":
    unittest.main()
