"""
Abstract notification service and concrete implementations for sending notifications.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class NotificationService(ABC):
    """Abstract base class for notification services."""

    @abstractmethod
    async def send_forgot_password(self, email: str, reset_token: str, **kwargs) -> bool:
        """Send forgot password notification.

        Args:
            email: User's email address
            reset_token: Password reset token
            **kwargs: Additional parameters for specific implementations

        Returns:
            bool: True if notification was sent successfully, False otherwise

        Raises:
            Exception: If sending fails
        """
        pass


class EmailNotificationService(NotificationService):
    """Email implementation of notification service."""

    def __init__(self, smtp_config: Dict[str, Any] = None):
        """Initialize email notification service.
        
        Args:
            smtp_config: Email configuration (host, port, username, password, etc.)
        """
        self.smtp_config = smtp_config or {}

    async def send_forgot_password(self, email: str, reset_token: str, **kwargs) -> bool:
        """Send forgot password email notification.

        Args:
            email: User's email address
            reset_token: Password reset token
            **kwargs: Additional email parameters (subject, template, etc.)

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # TODO: Implement actual email sending logic
            # For now, simulate email sending with logging
            subject = kwargs.get("subject", "Password Reset Request")
            reset_link = kwargs.get("reset_link", f"https://example.com/reset?token={reset_token}")
            
            print(f"[EMAIL] Sending password reset email to: {email}")
            print(f"[EMAIL] Subject: {subject}")
            print(f"[EMAIL] Reset link: {reset_link}")
            print(f"[EMAIL] Reset token: {reset_token}")
            
            # Simulate successful email sending
            return True
            
        except Exception as e:
            print(f"[EMAIL] Failed to send email to {email}: {str(e)}")
            return False


class SMSNotificationService(NotificationService):
    """SMS implementation of notification service."""

    def __init__(self, sms_config: Dict[str, Any] = None):
        """Initialize SMS notification service.
        
        Args:
            sms_config: SMS configuration (provider, api_key, sender_id, etc.)
        """
        self.sms_config = sms_config or {}

    async def send_forgot_password(self, email: str, reset_token: str, **kwargs) -> bool:
        """Send forgot password SMS notification.

        Args:
            email: User's email address (used to lookup phone number)
            reset_token: Password reset token
            **kwargs: Additional SMS parameters (phone_number, message_template, etc.)

        Returns:
            bool: True if SMS was sent successfully, False otherwise
        """
        try:
            # TODO: Implement actual SMS sending logic
            # For now, simulate SMS sending with logging
            phone_number = kwargs.get("phone_number", "+1234567890")  # Would normally lookup from user
            message = kwargs.get("message", f"Your password reset code: {reset_token[:8]}...")
            
            print(f"[SMS] Sending password reset SMS to: {phone_number}")
            print(f"[SMS] Message: {message}")
            print(f"[SMS] Reset token: {reset_token}")
            
            # Simulate successful SMS sending
            return True
            
        except Exception as e:
            print(f"[SMS] Failed to send SMS to {kwargs.get('phone_number', 'unknown')}: {str(e)}")
            return False