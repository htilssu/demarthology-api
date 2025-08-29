"""
Tests for JWT token utility functions.
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
import jwt

from app.utils.jwt_token import generate_token, verify_token, extract_token_from_header
from app.configs.setting import setting


class TestJWTTokenUtils(unittest.TestCase):
    """Test cases for JWT token generation and verification."""

    def setUp(self):
        """Set up test data."""
        self.test_user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }

    def test_generate_token(self):
        """Test that generate_token creates a valid JWT token."""
        token = generate_token(self.test_user_data)
        
        # Check that the token is a string
        self.assertIsInstance(token, str)
        
        # Check that the token can be decoded
        decoded = jwt.decode(token, setting.JWT_SECRET, algorithms=[setting.JWT_ALGORITHM])
        self.assertEqual(decoded["user_data"], self.test_user_data)

    def test_verify_token_valid(self):
        """Test that verify_token returns user data for valid tokens."""
        token = generate_token(self.test_user_data)
        result = verify_token(token)
        
        self.assertEqual(result, self.test_user_data)

    def test_verify_token_invalid(self):
        """Test that verify_token returns None for invalid tokens."""
        invalid_token = "invalid.token.here"
        result = verify_token(invalid_token)
        
        self.assertIsNone(result)

    def test_verify_token_expired(self):
        """Test that verify_token returns None for expired tokens."""
        # Create an expired token manually
        past_time = datetime.utcnow() - timedelta(hours=1)
        payload = {
            "user_data": self.test_user_data,
            "exp": past_time,
            "iat": datetime.utcnow() - timedelta(hours=2)
        }
        expired_token = jwt.encode(payload, setting.JWT_SECRET, algorithm=setting.JWT_ALGORITHM)
        
        result = verify_token(expired_token)
        self.assertIsNone(result)

    def test_extract_token_from_header_valid(self):
        """Test extracting token from valid Authorization header."""
        header = "Bearer abc123xyz"
        result = extract_token_from_header(header)
        
        self.assertEqual(result, "abc123xyz")

    def test_extract_token_from_header_invalid_format(self):
        """Test extracting token from invalid Authorization header format."""
        invalid_headers = [
            "Basic abc123xyz",  # Wrong scheme
            "Bearer",  # Missing token
            "Bearer token1 token2",  # Too many parts
            "abc123xyz",  # Missing scheme
            ""  # Empty header
        ]
        
        for header in invalid_headers:
            with self.subTest(header=header):
                result = extract_token_from_header(header)
                self.assertIsNone(result)

    def test_extract_token_from_header_none(self):
        """Test extracting token from None header."""
        result = extract_token_from_header(None)
        self.assertIsNone(result)

    def test_token_roundtrip(self):
        """Test generating and verifying token roundtrip."""
        # Generate token
        token = generate_token(self.test_user_data)
        
        # Verify token
        result = verify_token(token)
        
        # Should get back the same user data
        self.assertEqual(result, self.test_user_data)


if __name__ == "__main__":
    unittest.main()