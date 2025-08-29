from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException

from app.models.user import User
from app.schemas.auth_responses import ResetPasswordResponse
from app.schemas.reset_password_request import ResetPasswordRequest
from app.use_cases.reset_password_uc import ResetPasswordUC


class TestResetPasswordUC:
    """Test cases for ResetPasswordUC."""

    @pytest.fixture
    def mock_user_service(self):
        """Create a mock user service."""
        return Mock()

    @pytest.fixture
    def reset_password_uc(self, mock_user_service):
        """Create ResetPasswordUC instance with mocked dependencies."""
        return ResetPasswordUC(user_service=mock_user_service)

    @pytest.fixture
    def sample_user(self):
        """Create a sample user."""
        from unittest.mock import MagicMock

        mock_user = MagicMock(spec=User)
        mock_user.email = "user@example.com"
        mock_user.password = "old_hashed_password"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"
        return mock_user

    @pytest.mark.asyncio
    async def test_reset_password_success(self, reset_password_uc, mock_user_service, sample_user):
        """Test successful password reset."""
        # Arrange
        request = ResetPasswordRequest(
            token="valid_token",
            new_password="newpassword123",
            confirm_new_password="newpassword123",
        )

        with patch("app.use_cases.reset_password_uc.JWTUtils.decode_reset_token") as mock_decode:
            with patch("app.use_cases.reset_password_uc.PasswordUtils.hash_password") as mock_hash:
                mock_decode.return_value = "user@example.com"
                mock_hash.return_value = "new_hashed_password"
                mock_user_service.find_by_email = AsyncMock(return_value=sample_user)
                mock_user_service.save_user = AsyncMock()

                # Act
                response = await reset_password_uc.action(request)

                # Assert
                assert isinstance(response, ResetPasswordResponse)
                assert response.success is True
                assert "Password has been reset successfully" in response.message

                mock_decode.assert_called_once_with("valid_token")
                mock_user_service.find_by_email.assert_called_once_with("user@example.com")
                mock_hash.assert_called_once_with("newpassword123")
                mock_user_service.save_user.assert_called_once_with(sample_user)
                assert sample_user.password == "new_hashed_password"

    @pytest.mark.asyncio
    async def test_reset_password_invalid_token(self, reset_password_uc, mock_user_service):
        """Test password reset with invalid token."""
        # Arrange
        request = ResetPasswordRequest(
            token="invalid_token",
            new_password="newpassword123",
            confirm_new_password="newpassword123",
        )

        with patch("app.use_cases.reset_password_uc.JWTUtils.decode_reset_token") as mock_decode:
            mock_decode.side_effect = HTTPException(status_code=400, detail="Invalid reset token")

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await reset_password_uc.action(request)

            assert exc_info.value.status_code == 400
            assert "Invalid reset token" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_reset_password_user_not_found(self, reset_password_uc, mock_user_service):
        """Test password reset when user is not found."""
        # Arrange
        request = ResetPasswordRequest(
            token="valid_token",
            new_password="newpassword123",
            confirm_new_password="newpassword123",
        )

        with patch("app.use_cases.reset_password_uc.JWTUtils.decode_reset_token") as mock_decode:
            mock_decode.return_value = "nonexistent@example.com"
            mock_user_service.find_by_email = AsyncMock(return_value=None)

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await reset_password_uc.action(request)

            assert exc_info.value.status_code == 404
            assert "User not found" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_reset_password_empty_email_from_token(self, reset_password_uc, mock_user_service):
        """Test password reset when token contains no email."""
        # Arrange
        request = ResetPasswordRequest(
            token="valid_token_no_email",
            new_password="newpassword123",
            confirm_new_password="newpassword123",
        )

        with patch("app.use_cases.reset_password_uc.JWTUtils.decode_reset_token") as mock_decode:
            mock_decode.return_value = None

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await reset_password_uc.action(request)

            assert exc_info.value.status_code == 400
            assert "Invalid reset token" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_reset_password_service_error(self, reset_password_uc, mock_user_service, sample_user):
        """Test password reset when service throws error."""
        # Arrange
        request = ResetPasswordRequest(
            token="valid_token",
            new_password="newpassword123",
            confirm_new_password="newpassword123",
        )

        with patch("app.use_cases.reset_password_uc.JWTUtils.decode_reset_token") as mock_decode:
            mock_decode.return_value = "user@example.com"
            mock_user_service.find_by_email = AsyncMock(side_effect=Exception("Database error"))

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await reset_password_uc.action(request)

            assert exc_info.value.status_code == 500
            assert "Failed to reset password" in exc_info.value.detail
