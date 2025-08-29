from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException, Request

from app.models.user import User
from app.schemas.auth_responses import LogoutResponse
from app.use_cases.logout_uc import LogoutUC


class TestLogoutUC:
    """Test cases for LogoutUC."""

    @pytest.fixture
    def mock_current_user_service(self):
        """Create a mock current user service."""
        return Mock()

    @pytest.fixture
    def logout_uc(self, mock_current_user_service):
        """Create LogoutUC instance with mocked dependencies."""
        return LogoutUC(current_user_service=mock_current_user_service)

    @pytest.fixture
    def mock_request(self):
        """Create a mock request."""
        return Mock(spec=Request)

    @pytest.fixture
    def sample_user(self):
        """Create a sample user."""
        from unittest.mock import MagicMock

        mock_user = MagicMock(spec=User)
        mock_user.email = "user@example.com"
        mock_user.password = "hashed_password"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"
        return mock_user

    @pytest.mark.asyncio
    async def test_logout_success(self, logout_uc, mock_current_user_service, mock_request, sample_user):
        """Test successful logout."""
        # Arrange
        mock_current_user_service.get_current_user = AsyncMock(return_value=sample_user)

        # Act
        response = await logout_uc.action(mock_request)

        # Assert
        assert isinstance(response, LogoutResponse)
        assert response.success is True
        assert "Logged out successfully" in response.message
        mock_current_user_service.get_current_user.assert_called_once_with(mock_request)

    @pytest.mark.asyncio
    async def test_logout_invalid_token(self, logout_uc, mock_current_user_service, mock_request):
        """Test logout with invalid token."""
        # Arrange
        mock_current_user_service.get_current_user = AsyncMock(
            side_effect=HTTPException(status_code=401, detail="Invalid token")
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await logout_uc.action(mock_request)

        assert exc_info.value.status_code == 401
        assert "Invalid token" in exc_info.value.detail
        mock_current_user_service.get_current_user.assert_called_once_with(mock_request)

    @pytest.mark.asyncio
    async def test_logout_no_authorization_header(self, logout_uc, mock_current_user_service, mock_request):
        """Test logout without authorization header."""
        # Arrange
        mock_current_user_service.get_current_user = AsyncMock(
            side_effect=HTTPException(status_code=401, detail="Authorization header missing")
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await logout_uc.action(mock_request)

        assert exc_info.value.status_code == 401
        assert "Authorization header missing" in exc_info.value.detail
        mock_current_user_service.get_current_user.assert_called_once_with(mock_request)
