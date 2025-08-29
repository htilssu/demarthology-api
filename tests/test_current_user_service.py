"""
Tests for CurrentUserService.
"""

import unittest
from unittest.mock import Mock, patch, AsyncMock
import asyncio

from app.services.current_user_service import CurrentUserService
from app.errors.unauthorized import UnauthorizedException
from app.utils.jwt_token import generate_token
from app.models.user import User


class TestCurrentUserService(unittest.TestCase):
    """Test cases for CurrentUserService."""

    def setUp(self):
        """Set up test data."""
        # Mock the repository
        self.mock_repository = Mock()
        self.service = CurrentUserService(user_repository=self.mock_repository)
        
        self.test_user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
        self.valid_token = generate_token(self.test_user_data)
        
        # Create a mock User object
        self.mock_user = Mock(spec=User)
        self.mock_user.email = "test@example.com"
        self.mock_user.first_name = "John"
        self.mock_user.last_name = "Doe"

    async def async_test_get_current_user_valid_token(self):
        """Test get_current_user with valid Authorization header."""
        # Mock repository to return user
        self.mock_repository.find_by_email = AsyncMock(return_value=self.mock_user)
        
        # Mock request with valid Authorization header
        mock_request = Mock()
        mock_request.headers = {"Authorization": f"Bearer {self.valid_token}"}
        
        result = await self.service.get_current_user(mock_request)
        
        self.assertEqual(result, self.mock_user)
        self.mock_repository.find_by_email.assert_called_once_with("test@example.com")

    def test_get_current_user_valid_token(self):
        """Test get_current_user with valid Authorization header."""
        asyncio.run(self.async_test_get_current_user_valid_token())

    async def async_test_get_current_user_no_header(self):
        """Test get_current_user without Authorization header."""
        # Mock request without Authorization header
        mock_request = Mock()
        mock_request.headers = {}
        
        with self.assertRaises(UnauthorizedException) as context:
            await self.service.get_current_user(mock_request)
        
        self.assertEqual(context.exception.message, "Authorization header is required")

    def test_get_current_user_no_header(self):
        """Test get_current_user without Authorization header."""
        asyncio.run(self.async_test_get_current_user_no_header())

    async def async_test_get_current_user_invalid_header_format(self):
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
                    await self.service.get_current_user(mock_request)
                
                self.assertEqual(
                    context.exception.message, 
                    "Invalid Authorization header format. Expected: Bearer <token>"
                )

    def test_get_current_user_invalid_header_format(self):
        """Test get_current_user with invalid Authorization header format."""
        asyncio.run(self.async_test_get_current_user_invalid_header_format())

    async def async_test_get_current_user_invalid_token(self):
        """Test get_current_user with invalid token."""
        # Mock request with invalid token
        mock_request = Mock()
        mock_request.headers = {"Authorization": "Bearer invalid.token.here"}
        
        with self.assertRaises(UnauthorizedException) as context:
            await self.service.get_current_user(mock_request)
        
        self.assertEqual(context.exception.message, "Invalid or expired token")

    def test_get_current_user_invalid_token(self):
        """Test get_current_user with invalid token."""
        asyncio.run(self.async_test_get_current_user_invalid_token())

    async def async_test_get_current_user_user_not_found(self):
        """Test get_current_user when user not found in database."""
        # Mock repository to return None (user not found)
        self.mock_repository.find_by_email = AsyncMock(return_value=None)
        
        # Mock request with valid token
        mock_request = Mock()
        mock_request.headers = {"Authorization": f"Bearer {self.valid_token}"}
        
        with self.assertRaises(UnauthorizedException) as context:
            await self.service.get_current_user(mock_request)
        
        self.assertEqual(context.exception.message, "User not found")
        self.mock_repository.find_by_email.assert_called_once_with("test@example.com")

    def test_get_current_user_user_not_found(self):
        """Test get_current_user when user not found in database."""
        asyncio.run(self.async_test_get_current_user_user_not_found())

    async def async_test_get_current_user_from_token_valid(self):
        """Test get_current_user_from_token with valid token."""
        # Mock repository to return user
        self.mock_repository.find_by_email = AsyncMock(return_value=self.mock_user)
        
        result = await self.service.get_current_user_from_token(self.valid_token)
        
        self.assertEqual(result, self.mock_user)
        self.mock_repository.find_by_email.assert_called_once_with("test@example.com")

    def test_get_current_user_from_token_valid(self):
        """Test get_current_user_from_token with valid token."""
        asyncio.run(self.async_test_get_current_user_from_token_valid())

    async def async_test_get_current_user_from_token_invalid(self):
        """Test get_current_user_from_token with invalid token."""
        with self.assertRaises(UnauthorizedException) as context:
            await self.service.get_current_user_from_token("invalid.token.here")
        
        self.assertEqual(context.exception.message, "Invalid or expired token")

    def test_get_current_user_from_token_invalid(self):
        """Test get_current_user_from_token with invalid token."""
        asyncio.run(self.async_test_get_current_user_from_token_invalid())

    @patch('app.services.current_user_service.verify_token')
    async def async_test_get_current_user_expired_token(self, mock_verify_token):
        """Test get_current_user with expired token."""
        # Mock verify_token to return None (expired token)
        mock_verify_token.return_value = None
        
        mock_request = Mock()
        mock_request.headers = {"Authorization": f"Bearer {self.valid_token}"}
        
        with self.assertRaises(UnauthorizedException) as context:
            await self.service.get_current_user(mock_request)
        
        self.assertEqual(context.exception.message, "Invalid or expired token")

    def test_get_current_user_expired_token(self):
        """Test get_current_user with expired token."""
        asyncio.run(self.async_test_get_current_user_expired_token())


if __name__ == "__main__":
    unittest.main()