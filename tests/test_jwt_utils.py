import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

from fastapi import HTTPException

from app.utils.jwt import JWTUtils


class TestJWTUtils:
    """Test cases for JWT utilities."""

    def test_create_access_token(self):
        """Test creating an access token."""
        data = {"email": "test@example.com", "user_id": "123"}

        token = JWTUtils.create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_access_token_success(self):
        """Test decoding a valid access token."""
        data = {"email": "test@example.com", "user_id": "123"}
        token = JWTUtils.create_access_token(data)

        decoded = JWTUtils.decode_access_token(token)

        assert decoded["email"] == "test@example.com"
        assert decoded["user_id"] == "123"
        assert "exp" in decoded

    def test_decode_access_token_invalid_token(self):
        """Test decoding an invalid token."""
        with pytest.raises(HTTPException) as exc_info:
            JWTUtils.decode_access_token("invalid-token")

        assert exc_info.value.status_code == 401
        assert "Invalid token" in exc_info.value.detail

    @patch("app.utils.jwt.datetime")
    def test_decode_access_token_expired_token(self, mock_datetime):
        """Test decoding an expired token."""
        # Create a token that's already expired
        past_time = datetime.now(timezone.utc) - timedelta(hours=1)
        mock_datetime.now.return_value = past_time

        data = {"email": "test@example.com", "user_id": "123"}
        token = JWTUtils.create_access_token(data)

        # Reset datetime to current time
        mock_datetime.now.return_value = datetime.now(timezone.utc)

        with pytest.raises(HTTPException) as exc_info:
            JWTUtils.decode_access_token(token)

        assert exc_info.value.status_code == 401
        assert "Token has expired" in exc_info.value.detail
