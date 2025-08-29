"""
Tests for CurrentUserService.
"""

import unittest
from unittest.mock import Mock, patch

from app.services.current_user_service import CurrentUserService
from app.errors.unauthorized import UnauthorizedException
from app.utils.jwt_token import generate_token


class TestCurrentUserService(unittest.TestCase):
    """Test cases for CurrentUserService."""

    def setUp(self):
        """Set up test data."""
        self.service = CurrentUserService()
        self.test_user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
        self.valid_token = generate_token(self.test_user_data)

    def test_get_current_user_valid_token(self):
        """Test get_current_user with valid Authorization header."""
        # Mock request with valid Authorization header
        mock_request = Mock()
        mock_request.headers = {"Authorization": f"Bearer {self.valid_token}"}
        
        result = self.service.get_current_user(mock_request)
        
        self.assertEqual(result, self.test_user_data)

    def test_get_current_user_no_header(self):
        """Test get_current_user without Authorization header."""
        # Mock request without Authorization header
        mock_request = Mock()
        mock_request.headers = {}
        
        with self.assertRaises(UnauthorizedException) as context:
            self.service.get_current_user(mock_request)
        
        self.assertEqual(context.exception.message, "Authorization header is required")

    def test_get_current_user_invalid_header_format(self):
        """Test get_current_user with invalid Authorization header format."""
        invalid_headers = [
            "Basic token123",  # Wrong scheme
            "Bearer",  # Missing token
            "token123",  # Missing scheme
            "Bearer token1 token2"  # Too many parts
        ]
        
        for header in invalid_headers:
            with self.subTest(header=header):
                mock_request = Mock()
                mock_request.headers = {"Authorization": header}
                
                with self.assertRaises(UnauthorizedException) as context:
                    self.service.get_current_user(mock_request)
                
                self.assertEqual(
                    context.exception.message, 
                    "Invalid Authorization header format. Expected: Bearer <token>"
                )

    def test_get_current_user_invalid_token(self):
        """Test get_current_user with invalid token."""
        # Mock request with invalid token
        mock_request = Mock()
        mock_request.headers = {"Authorization": "Bearer invalid.token.here"}
        
        with self.assertRaises(UnauthorizedException) as context:
            self.service.get_current_user(mock_request)
        
        self.assertEqual(context.exception.message, "Invalid or expired token")

    def test_get_current_user_from_token_valid(self):
        """Test get_current_user_from_token with valid token."""
        result = self.service.get_current_user_from_token(self.valid_token)
        
        self.assertEqual(result, self.test_user_data)

    def test_get_current_user_from_token_invalid(self):
        """Test get_current_user_from_token with invalid token."""
        with self.assertRaises(UnauthorizedException) as context:
            self.service.get_current_user_from_token("invalid.token.here")
        
        self.assertEqual(context.exception.message, "Invalid or expired token")

    @patch('app.services.current_user_service.verify_token')
    def test_get_current_user_expired_token(self, mock_verify_token):
        """Test get_current_user with expired token."""
        # Mock verify_token to return None (expired token)
        mock_verify_token.return_value = None
        
        mock_request = Mock()
        mock_request.headers = {"Authorization": f"Bearer {self.valid_token}"}
        
        with self.assertRaises(UnauthorizedException) as context:
            self.service.get_current_user(mock_request)
        
        self.assertEqual(context.exception.message, "Invalid or expired token")


if __name__ == "__main__":
    unittest.main()