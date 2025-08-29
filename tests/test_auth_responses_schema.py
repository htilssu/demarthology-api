import pytest

from app.schemas.auth_responses import (
    ForgotPasswordResponse,
    LogoutResponse,
    ResetPasswordResponse,
)


class TestAuthResponseSchemas:
    """Test cases for authentication response schemas."""

    def test_forgot_password_response_creation(self):
        """Test creating a forgot password response."""
        response = ForgotPasswordResponse(success=True, message="Reset link sent")

        assert response.success is True
        assert response.message == "Reset link sent"

    def test_forgot_password_response_serialization(self):
        """Test serialization of forgot password response."""
        response = ForgotPasswordResponse(success=False, message="Email not found")

        serialized = response.model_dump()
        expected = {"success": False, "message": "Email not found"}
        assert serialized == expected

    def test_reset_password_response_creation(self):
        """Test creating a reset password response."""
        response = ResetPasswordResponse(success=True, message="Password reset successfully")

        assert response.success is True
        assert response.message == "Password reset successfully"

    def test_reset_password_response_serialization(self):
        """Test serialization of reset password response."""
        response = ResetPasswordResponse(success=False, message="Invalid reset token")

        serialized = response.model_dump()
        expected = {"success": False, "message": "Invalid reset token"}
        assert serialized == expected

    def test_logout_response_creation(self):
        """Test creating a logout response."""
        response = LogoutResponse(success=True, message="Logged out successfully")

        assert response.success is True
        assert response.message == "Logged out successfully"

    def test_logout_response_serialization(self):
        """Test serialization of logout response."""
        response = LogoutResponse(success=True, message="Session terminated")

        serialized = response.model_dump()
        expected = {"success": True, "message": "Session terminated"}
        assert serialized == expected
