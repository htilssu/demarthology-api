import pytest
from pydantic import ValidationError

from app.schemas.forgot_password_request import ForgotPasswordRequest


class TestForgotPasswordRequestSchema:
    """Test cases for ForgotPasswordRequest schema."""

    def test_valid_forgot_password_request(self):
        """Test creating a valid forgot password request."""
        data = {"email": "test@example.com"}
        request = ForgotPasswordRequest(**data)

        assert request.email == "test@example.com"

    def test_invalid_email_format(self):
        """Test forgot password request with invalid email format."""
        data = {"email": "invalid-email"}

        with pytest.raises(ValidationError) as exc_info:
            ForgotPasswordRequest(**data)

        assert "valid email" in str(exc_info.value)

    def test_missing_email_field(self):
        """Test forgot password request without email field."""
        data = {}

        with pytest.raises(ValidationError) as exc_info:
            ForgotPasswordRequest(**data)

        assert "email" in str(exc_info.value)
        assert "required" in str(exc_info.value)

    def test_forgot_password_request_serialization(self):
        """Test serialization of forgot password request."""
        data = {"email": "user@domain.com"}
        request = ForgotPasswordRequest(**data)

        serialized = request.model_dump()
        assert serialized == {"email": "user@domain.com"}
