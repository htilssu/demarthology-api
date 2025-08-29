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

    def test_create_reset_token(self):
        """Test creating a password reset token."""
        email = "user@example.com"
        token = JWTUtils.create_reset_token(email)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_reset_token_success(self):
        """Test successfully decoding a reset token."""
        email = "user@example.com"
        token = JWTUtils.create_reset_token(email)

        decoded_email = JWTUtils.decode_reset_token(token)

        assert decoded_email == email

    def test_decode_reset_token_invalid_token(self):
        """Test decoding an invalid reset token."""
        invalid_token = "invalid.reset.token"

        with pytest.raises(HTTPException) as exc_info:
            JWTUtils.decode_reset_token(invalid_token)

        assert exc_info.value.status_code == 400
        assert "Invalid reset token" in exc_info.value.detail

    @patch("app.utils.jwt.datetime")
    def test_decode_reset_token_expired_token(self, mock_datetime):
        """Test decoding an expired reset token."""
        # Create a token that's already expired
        past_time = datetime.now(timezone.utc) - timedelta(hours=1)
        mock_datetime.now.return_value = past_time

        email = "user@example.com"
        expired_token = JWTUtils.create_reset_token(email)

        # Reset datetime to current time
        mock_datetime.now.return_value = datetime.now(timezone.utc)

        with pytest.raises(HTTPException) as exc_info:
            JWTUtils.decode_reset_token(expired_token)

        assert exc_info.value.status_code == 400
        assert "Reset token has expired" in exc_info.value.detail

    def test_decode_reset_token_wrong_type(self):
        """Test decoding a token with wrong type."""
        # Create an access token instead of reset token
        data = {"email": "user@example.com", "type": "access"}
        access_token = JWTUtils.create_access_token(data)

        with pytest.raises(HTTPException) as exc_info:
            JWTUtils.decode_reset_token(access_token)

        assert exc_info.value.status_code == 400
        assert "Invalid token type" in exc_info.value.detail

    def test_reset_token_expires_faster_than_access_token(self):
        """Test that reset tokens expire faster than access tokens."""
        assert (
            JWTUtils.RESET_TOKEN_EXPIRE_MINUTES < JWTUtils.ACCESS_TOKEN_EXPIRE_MINUTES
        )
