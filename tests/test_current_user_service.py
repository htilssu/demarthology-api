import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from bson import ObjectId

from fastapi import HTTPException

from app.services.current_user_service import CurrentUserService
from app.models.user import User


class TestCurrentUserService:
    """Test cases for CurrentUserService."""

    @pytest.fixture
    def mock_user_service(self):
        """Create a mock UserService."""
        return Mock()

    @pytest.fixture
    def mock_session_provider(self):
        """Create a mock SessionProvider."""
        return Mock()

    @pytest.fixture
    def mock_request(self):
        """Create a mock request object."""
        return Mock()

    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        user = Mock(spec=User)
        user.id = ObjectId()
        user.email = "test@example.com"
        user.password = "hashed_password"
        user.first_name = "John"
        user.last_name = "Doe"
        user.dob = datetime(1990, 1, 1)
        return user

    @pytest.fixture
    def current_user_service(self, mock_user_service, mock_session_provider):
        """Create a CurrentUserService instance with mocked dependencies."""
        return CurrentUserService(
            user_service=mock_user_service, session_provider=mock_session_provider
        )

    @pytest.mark.asyncio
    async def test_get_current_user_success(
        self, current_user_service, mock_request, sample_user
    ):
        """Test successful current user retrieval."""
        # Mock session provider to return session data
        session_data = {"email": "test@example.com", "user_id": str(sample_user.id)}
        current_user_service._session_provider.get_session = AsyncMock(
            return_value=session_data
        )

        # Mock user service to return user
        current_user_service._user_service.find_by_email = AsyncMock(
            return_value=sample_user
        )

        result = await current_user_service.get_current_user(mock_request)

        assert result == sample_user
        current_user_service._session_provider.get_session.assert_called_once_with(
            mock_request
        )
        current_user_service._user_service.find_by_email.assert_called_once_with(
            "test@example.com"
        )

    @pytest.mark.asyncio
    async def test_get_current_user_no_email_in_session(
        self, current_user_service, mock_request
    ):
        """Test when email is missing from session data."""
        # Mock session provider to return session data without email
        session_data = {"user_id": "user123"}
        current_user_service._session_provider.get_session = AsyncMock(
            return_value=session_data
        )

        with pytest.raises(HTTPException) as exc_info:
            await current_user_service.get_current_user(mock_request)

        assert exc_info.value.status_code == 401
        assert "User email not found in session" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_current_user_user_not_found(
        self, current_user_service, mock_request
    ):
        """Test when user is not found in database."""
        # Mock session provider to return session data
        session_data = {"email": "test@example.com", "user_id": "user123"}
        current_user_service._session_provider.get_session = AsyncMock(
            return_value=session_data
        )

        # Mock user service to return None (user not found)
        current_user_service._user_service.find_by_email = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            await current_user_service.get_current_user(mock_request)

        assert exc_info.value.status_code == 401
        assert "User not found" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_current_user_session_provider_error(
        self, current_user_service, mock_request
    ):
        """Test when session provider raises an error."""
        # Mock session provider to raise HTTPException
        current_user_service._session_provider.get_session = AsyncMock(
            side_effect=HTTPException(status_code=401, detail="Invalid token")
        )

        with pytest.raises(HTTPException) as exc_info:
            await current_user_service.get_current_user(mock_request)

        assert exc_info.value.status_code == 401
        assert "Invalid token" in exc_info.value.detail
