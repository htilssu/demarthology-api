"""
Integration test for login with JWT token generation.
"""

import unittest
from unittest.mock import AsyncMock, MagicMock

from app.models.user import User
from app.schemas.login_request import LoginRequest
from app.services.user_service import UserService
from app.use_cases.login_uc import LoginUC
from app.utils.jwt import JWTUtils
from app.utils.password import hash_password


class TestLoginWithJWT(unittest.IsolatedAsyncioTestCase):
    """Integration test for login with JWT token generation."""

    def setUp(self):
        """Set up test data."""
        self.mock_user_service = AsyncMock(spec=UserService)
        self.login_uc = LoginUC(user_service=self.mock_user_service)

    async def test_login_generates_jwt_token(self):
        """Test that successful login generates a valid JWT token."""
        # Arrange
        test_password = "testpassword123"
        hashed_password = hash_password(test_password)

        mock_user = MagicMock(spec=User)
        mock_user.id = "507f1f77bcf86cd799439011"  # Mock ObjectId
        mock_user.email = "test@example.com"
        mock_user.password = hashed_password
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"  # String role value

        self.mock_user_service.find_by_email.return_value = mock_user

        login_request = LoginRequest(email="test@example.com", password=test_password)

        # Act
        result = await self.login_uc.action(login_request)

        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Đăng nhập thành công")
        self.assertIsNotNone(result.access_token)
        self.assertEqual(result.token_type, "bearer")

        # Verify the token contains correct user data
        token = result.access_token
        user_data = JWTUtils.decode_access_token(token)

        self.assertIsNotNone(user_data)
        self.assertEqual(user_data["email"], "test@example.com")
        self.assertEqual(user_data["user_id"], "507f1f77bcf86cd799439011")


if __name__ == "__main__":
    unittest.main()
