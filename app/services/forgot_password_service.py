"""
Forgot password service that handles password reset functionality.
"""

from typing import Optional
from fastapi import Depends

from app.services.notification_service import NotificationService, EmailNotificationService
from app.services.user_service import UserService
from app.utils.jwt import JWTUtils


class ForgotPasswordService:
    """Service for handling forgot password operations."""

    def __init__(
        self,
        user_service: UserService = Depends(UserService),
        notification_service: NotificationService = Depends(EmailNotificationService),
    ):
        """Initialize forgot password service.

        Args:
            user_service: Service for user operations
            notification_service: Service for sending notifications
        """
        self._user_service = user_service
        self._notification_service = notification_service

    async def send_forgot_password_notification(
        self,
        email: str,
        notification_type: str = "email",
        **kwargs
    ) -> bool:
        """Send forgot password notification to user.

        Args:
            email: User's email address
            notification_type: Type of notification ("email" or "sms")
            **kwargs: Additional parameters for notification

        Returns:
            bool: True if notification was sent successfully

        Raises:
            Exception: If user doesn't exist or notification fails
        """
        try:
            # Check if user exists
            user_exists = await self._user_service.check_user_exist(email)
            
            if not user_exists:
                # For security, we don't reveal if user exists
                # But we still return True to not leak information
                return True
            
            # Generate reset token
            reset_token = JWTUtils.create_reset_token(email)
            
            # Send notification
            success = await self._notification_service.send_forgot_password(
                email=email,
                reset_token=reset_token,
                **kwargs
            )
            return success
            
        except Exception as e:
            # Log error but don't expose details for security
            print(f"Failed to send forgot password notification to {email}: {str(e)}")
            return False

    async def verify_reset_token(self, token: str) -> Optional[str]:
        """Verify reset token and return email if valid.

        Args:
            token: JWT reset token

        Returns:
            str: Email address if token is valid, None otherwise
        """
        try:
            # Decode and verify the token
            payload = JWTUtils.verify_reset_token(token)
            return payload.get("email") if payload else None
        except Exception:
            return None