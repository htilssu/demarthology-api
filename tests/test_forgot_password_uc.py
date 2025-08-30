from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException

from app.schemas.auth_responses import ForgotPasswordResponse
from app.schemas.forgot_password_request import ForgotPasswordRequest
from app.use_cases.forgot_password_uc import ForgotPasswordUC


class TestForgotPasswordUC:
    """Test cases for ForgotPasswordUC."""

    @pytest.fixture
    def mock_forgot_password_service(self):
        """Create a mock forgot password service."""
        return Mock()

    @pytest.fixture
    def forgot_password_uc(self, mock_forgot_password_service):
        """Create ForgotPasswordUC instance with mocked dependencies."""
        return ForgotPasswordUC(forgot_password_service=mock_forgot_password_service)

    @pytest.mark.asyncio
    async def test_forgot_password_user_exists(self, forgot_password_uc, mock_forgot_password_service):
        """Test forgot password when user exists."""
        # Arrange
        request = ForgotPasswordRequest(email="user@example.com")
        mock_forgot_password_service.send_forgot_password_notification = AsyncMock(return_value=True)

        # Act
        response = await forgot_password_uc.action(request)

        # Assert
        assert isinstance(response, ForgotPasswordResponse)
        assert response.success is True
        assert "reset link has been sent" in response.message
        mock_forgot_password_service.send_forgot_password_notification.assert_called_once_with(
            email="user@example.com", 
            notification_type="email"
        )

    @pytest.mark.asyncio
    async def test_forgot_password_user_not_exists(self, forgot_password_uc, mock_forgot_password_service):
        """Test forgot password when user doesn't exist."""
        # Arrange
        request = ForgotPasswordRequest(email="nonexistent@example.com")
        mock_forgot_password_service.send_forgot_password_notification = AsyncMock(return_value=True)

        # Act
        response = await forgot_password_uc.action(request)

        # Assert
        assert isinstance(response, ForgotPasswordResponse)
        assert response.success is True
        # Should return same message for security (don't reveal if email exists)
        assert "reset link has been sent" in response.message
        mock_forgot_password_service.send_forgot_password_notification.assert_called_once_with(
            email="nonexistent@example.com",
            notification_type="email"
        )

    @pytest.mark.asyncio
    async def test_forgot_password_service_error(self, forgot_password_uc, mock_forgot_password_service):
        """Test forgot password when service throws error."""
        # Arrange
        request = ForgotPasswordRequest(email="user@example.com")
        mock_forgot_password_service.send_forgot_password_notification = AsyncMock(side_effect=Exception("Service error"))

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await forgot_password_uc.action(request)

        assert exc_info.value.status_code == 500
        assert "Failed to process forgot password request" in exc_info.value.detail
