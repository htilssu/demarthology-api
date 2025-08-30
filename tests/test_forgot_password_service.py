"""
Tests for forgot password service.
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from app.services.forgot_password_service import ForgotPasswordService


class TestForgotPasswordService:
    """Test cases for ForgotPasswordService."""

    @pytest.fixture
    def mock_user_service(self):
        """Create a mock user service."""
        return Mock()

    @pytest.fixture
    def mock_notification_service(self):
        """Create a mock notification service."""
        mock = Mock()
        mock.send_forgot_password = AsyncMock()
        return mock

    @pytest.fixture
    def forgot_password_service(self, mock_user_service, mock_notification_service):
        """Create ForgotPasswordService instance with mocked dependencies."""
        return ForgotPasswordService(
            user_service=mock_user_service,
            notification_service=mock_notification_service
        )

    @pytest.mark.asyncio
    async def test_send_notification_user_exists_success(
        self, forgot_password_service, mock_user_service, mock_notification_service
    ):
        """Test sending notification when user exists and notification succeeds."""
        # Arrange
        email = "user@example.com"
        mock_user_service.check_user_exist = AsyncMock(return_value=True)
        mock_notification_service.send_forgot_password.return_value = True

        # Act
        result = await forgot_password_service.send_forgot_password_notification(email)

        # Assert
        assert result is True
        mock_user_service.check_user_exist.assert_called_once_with(email)
        mock_notification_service.send_forgot_password.assert_called_once()

        # Check that the notification was called with correct parameters
        call_args = mock_notification_service.send_forgot_password.call_args
        assert call_args.kwargs['email'] == email
        assert 'reset_token' in call_args.kwargs
        assert call_args.kwargs['reset_token'] is not None

    @pytest.mark.asyncio
    async def test_send_notification_user_not_exists(
        self, forgot_password_service, mock_user_service, mock_notification_service
    ):
        """Test sending notification when user doesn't exist (should still return True for security)."""
        # Arrange
        email = "nonexistent@example.com"
        mock_user_service.check_user_exist = AsyncMock(return_value=False)

        # Act
        result = await forgot_password_service.send_forgot_password_notification(email)

        # Assert
        assert result is True
        mock_user_service.check_user_exist.assert_called_once_with(email)
        # Notification should not be called when user doesn't exist
        mock_notification_service.send_forgot_password.assert_not_called()

    @pytest.mark.asyncio
    async def test_send_notification_user_exists_notification_fails(
        self, forgot_password_service, mock_user_service, mock_notification_service
    ):
        """Test sending notification when user exists but notification fails."""
        # Arrange
        email = "user@example.com"
        mock_user_service.check_user_exist = AsyncMock(return_value=True)
        mock_notification_service.send_forgot_password.return_value = False

        # Act
        result = await forgot_password_service.send_forgot_password_notification(email)

        # Assert
        assert result is False
        mock_user_service.check_user_exist.assert_called_once_with(email)
        mock_notification_service.send_forgot_password.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_notification_user_service_error(
        self, forgot_password_service, mock_user_service, mock_notification_service
    ):
        """Test sending notification when user service throws error."""
        # Arrange
        email = "user@example.com"
        mock_user_service.check_user_exist = AsyncMock(side_effect=Exception("Database error"))

        # Act
        result = await forgot_password_service.send_forgot_password_notification(email)

        # Assert
        assert result is False
        mock_user_service.check_user_exist.assert_called_once_with(email)
        mock_notification_service.send_forgot_password.assert_not_called()

    @pytest.mark.asyncio
    async def test_send_notification_with_additional_kwargs(
        self, forgot_password_service, mock_user_service, mock_notification_service
    ):
        """Test sending notification with additional parameters."""
        # Arrange
        email = "user@example.com"
        mock_user_service.check_user_exist = AsyncMock(return_value=True)
        mock_notification_service.send_forgot_password.return_value = True

        additional_params = {
            "subject": "Custom Reset Subject",
            "reset_link": "https://custom.com/reset",
            "phone_number": "+1234567890"
        }

        # Act
        result = await forgot_password_service.send_forgot_password_notification(
            email, 
            notification_type="email",
            **additional_params
        )

        # Assert
        assert result is True
        call_args = mock_notification_service.send_forgot_password.call_args
        assert call_args.kwargs['email'] == email
        assert call_args.kwargs['subject'] == "Custom Reset Subject"
        assert call_args.kwargs['reset_link'] == "https://custom.com/reset"
        assert call_args.kwargs['phone_number'] == "+1234567890"

    @pytest.mark.asyncio
    async def test_send_notification_exception_handling(
        self, forgot_password_service, mock_user_service, mock_notification_service
    ):
        """Test exception handling during notification sending."""
        # Arrange
        email = "user@example.com"
        mock_user_service.check_user_exist = AsyncMock(return_value=True)
        mock_notification_service.send_forgot_password.side_effect = Exception("Notification error")

        # Act
        result = await forgot_password_service.send_forgot_password_notification(email)

        # Assert
        assert result is False
        mock_user_service.check_user_exist.assert_called_once_with(email)
        mock_notification_service.send_forgot_password.assert_called_once()

    @pytest.mark.asyncio
    async def test_verify_reset_token_valid(self, forgot_password_service):
        """Test verifying a valid reset token."""
        # Arrange
        valid_token = "valid_jwt_token"
        expected_payload = {"email": "user@example.com", "type": "reset"}

        with patch('app.services.forgot_password_service.JWTUtils.verify_reset_token') as mock_verify:
            mock_verify.return_value = expected_payload

            # Act
            result = await forgot_password_service.verify_reset_token(valid_token)

            # Assert
            assert result == "user@example.com"
            mock_verify.assert_called_once_with(valid_token)

    @pytest.mark.asyncio
    async def test_verify_reset_token_invalid(self, forgot_password_service):
        """Test verifying an invalid reset token."""
        # Arrange
        invalid_token = "invalid_jwt_token"

        with patch('app.services.forgot_password_service.JWTUtils.verify_reset_token') as mock_verify:
            mock_verify.return_value = None

            # Act
            result = await forgot_password_service.verify_reset_token(invalid_token)

            # Assert
            assert result is None
            mock_verify.assert_called_once_with(invalid_token)

    @pytest.mark.asyncio
    async def test_verify_reset_token_exception(self, forgot_password_service):
        """Test verifying reset token when JWT utils throws exception."""
        # Arrange
        token = "problematic_token"

        with patch('app.services.forgot_password_service.JWTUtils.verify_reset_token') as mock_verify:
            mock_verify.side_effect = Exception("JWT error")

            # Act
            result = await forgot_password_service.verify_reset_token(token)

            # Assert
            assert result is None
            mock_verify.assert_called_once_with(token)