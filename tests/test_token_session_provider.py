import pytest
from unittest.mock import Mock, patch

from fastapi import HTTPException

from app.services.token_session_provider import TokenSessionProvider
from app.utils.jwt import JWTUtils


class TestTokenSessionProvider:
    """Test cases for TokenSessionProvider."""

    @pytest.fixture
    def provider(self):
        """Create a TokenSessionProvider instance."""
        return TokenSessionProvider()

    @pytest.fixture
    def mock_request(self):
        """Create a mock request object."""
        request = Mock()
        request.headers = {}
        return request

    @pytest.mark.asyncio
    async def test_get_session_success(self, provider, mock_request):
        """Test successful session retrieval."""
        # Create a valid token
        data = {"email": "test@example.com", "user_id": "123"}
        token = JWTUtils.create_access_token(data)

        # Set up request with valid authorization header
        mock_request.headers = {"Authorization": f"Bearer {token}"}

        session = await provider.get_session(mock_request)

        assert session["email"] == "test@example.com"
        assert session["user_id"] == "123"

    @pytest.mark.asyncio
    async def test_get_session_missing_authorization_header(
        self, provider, mock_request
    ):
        """Test missing authorization header."""
        mock_request.headers = {}

        with pytest.raises(HTTPException) as exc_info:
            await provider.get_session(mock_request)

        assert exc_info.value.status_code == 401
        assert "Authorization header missing" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_session_invalid_authorization_format(
        self, provider, mock_request
    ):
        """Test invalid authorization header format."""
        mock_request.headers = {"Authorization": "InvalidFormat token"}

        with pytest.raises(HTTPException) as exc_info:
            await provider.get_session(mock_request)

        assert exc_info.value.status_code == 401
        assert "Authorization header must start with 'Bearer '" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_session_invalid_token(self, provider, mock_request):
        """Test invalid token."""
        mock_request.headers = {"Authorization": "Bearer invalid-token"}

        with pytest.raises(HTTPException) as exc_info:
            await provider.get_session(mock_request)

        assert exc_info.value.status_code == 401
        assert "Invalid token" in exc_info.value.detail
