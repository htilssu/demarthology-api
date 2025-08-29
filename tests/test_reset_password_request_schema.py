import pytest
from pydantic import ValidationError

from app.schemas.reset_password_request import ResetPasswordRequest


class TestResetPasswordRequestSchema:
    """Test cases for ResetPasswordRequest schema."""

    def test_valid_reset_password_request(self):
        """Test creating a valid reset password request."""
        data = {
            "token": "valid_reset_token",
            "new_password": "newpassword123",
            "confirm_new_password": "newpassword123",
        }
        request = ResetPasswordRequest(**data)

        assert request.token == "valid_reset_token"
        assert request.new_password == "newpassword123"
        assert request.confirm_new_password == "newpassword123"

    def test_passwords_do_not_match(self):
        """Test reset password request with non-matching passwords."""
        data = {
            "token": "valid_reset_token",
            "new_password": "password123",
            "confirm_new_password": "different123",
        }

        with pytest.raises(ValidationError) as exc_info:
            ResetPasswordRequest(**data)

        assert "Passwords do not match" in str(exc_info.value)

    def test_missing_required_fields(self):
        """Test reset password request with missing required fields."""
        data = {"token": "token_only"}

        with pytest.raises(ValidationError) as exc_info:
            ResetPasswordRequest(**data)

        error_str = str(exc_info.value)
        assert "new_password" in error_str
        assert "confirm_new_password" in error_str

    def test_reset_password_request_serialization(self):
        """Test serialization of reset password request."""
        data = {
            "token": "reset_token_123",
            "new_password": "secretpass",
            "confirm_new_password": "secretpass",
        }
        request = ResetPasswordRequest(**data)

        serialized = request.model_dump()
        expected = {
            "token": "reset_token_123",
            "new_password": "secretpass",
            "confirm_new_password": "secretpass",
        }
        assert serialized == expected
