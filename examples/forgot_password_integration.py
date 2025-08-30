"""
Example of how to configure and use the forgot password service with different notification providers.
This demonstrates the flexibility of the abstract notification service design.
"""

from fastapi import Depends, FastAPI
from app.services.notification_service import EmailNotificationService, SMSNotificationService
from app.services.forgot_password_service import ForgotPasswordService
from app.services.user_service import UserService
from app.schemas.forgot_password_request import ForgotPasswordRequest
from app.schemas.auth_responses import ForgotPasswordResponse

app = FastAPI()

# Configuration for different notification providers
EMAIL_CONFIG = {
    "host": "smtp.gmail.com",
    "port": 587,
    "username": "noreply@yourapp.com",
    "password": "your-email-password",
    "use_tls": True
}

SMS_CONFIG = {
    "provider": "twilio",
    "account_sid": "your-twilio-sid",
    "auth_token": "your-twilio-token",
    "from_number": "+1234567890"
}


def get_email_notification_service():
    """Factory function for email notification service."""
    return EmailNotificationService(smtp_config=EMAIL_CONFIG)


def get_sms_notification_service():
    """Factory function for SMS notification service."""
    return SMSNotificationService(sms_config=SMS_CONFIG)


def get_email_forgot_password_service(
    user_service: UserService = Depends(UserService),
    notification_service: EmailNotificationService = Depends(get_email_notification_service)
):
    """Factory function for forgot password service with email notifications."""
    return ForgotPasswordService(
        user_service=user_service,
        notification_service=notification_service
    )


def get_sms_forgot_password_service(
    user_service: UserService = Depends(UserService),
    notification_service: SMSNotificationService = Depends(get_sms_notification_service)
):
    """Factory function for forgot password service with SMS notifications."""
    return ForgotPasswordService(
        user_service=user_service,
        notification_service=notification_service
    )


@app.post("/auth/forgot-password/email", response_model=ForgotPasswordResponse)
async def forgot_password_email(
    request: ForgotPasswordRequest,
    service: ForgotPasswordService = Depends(get_email_forgot_password_service)
):
    """Endpoint for forgot password via email."""
    try:
        await service.send_forgot_password_notification(
            email=str(request.email),
            notification_type="email",
            subject="Reset Your Password",
            reset_link=f"https://yourapp.com/reset-password?email={request.email}"
        )
        
        return ForgotPasswordResponse(
            success=True,
            message="If the email exists, a password reset link has been sent"
        )
    except Exception:
        return ForgotPasswordResponse(
            success=False,
            message="Failed to process forgot password request"
        )


@app.post("/auth/forgot-password/sms", response_model=ForgotPasswordResponse)
async def forgot_password_sms(
    request: ForgotPasswordRequest,
    service: ForgotPasswordService = Depends(get_sms_forgot_password_service)
):
    """Endpoint for forgot password via SMS."""
    try:
        # In a real app, you'd lookup the user's phone number from their email
        # For demo purposes, we'll use a placeholder
        await service.send_forgot_password_notification(
            email=str(request.email),
            notification_type="sms",
            phone_number="+1234567890",  # Would be looked up from user profile
            message="Your password reset code will expire in 15 minutes."
        )
        
        return ForgotPasswordResponse(
            success=True,
            message="If the email exists, a password reset code has been sent via SMS"
        )
    except Exception:
        return ForgotPasswordResponse(
            success=False,
            message="Failed to process forgot password request"
        )


# Example of how to easily switch notification providers based on user preference
@app.post("/auth/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password_flexible(
    request: ForgotPasswordRequest,
    notification_type: str = "email",  # Could come from user preference
    user_service: UserService = Depends(UserService)
):
    """
    Flexible endpoint that can use either email or SMS based on user preference.
    This demonstrates the power of the abstract notification service design.
    """
    try:
        # Choose notification service based on user preference
        if notification_type == "sms":
            notification_service = get_sms_notification_service()
            extra_params = {
                "phone_number": "+1234567890",  # Would be from user profile
                "message": "Your reset code will expire in 15 minutes."
            }
        else:  # Default to email
            notification_service = get_email_notification_service()
            extra_params = {
                "subject": "Password Reset Request",
                "reset_link": f"https://yourapp.com/reset?email={request.email}"
            }
        
        # Create service with chosen notification provider
        service = ForgotPasswordService(
            user_service=user_service,
            notification_service=notification_service
        )
        
        # Send notification
        await service.send_forgot_password_notification(
            email=str(request.email),
            notification_type=notification_type,
            **extra_params
        )
        
        return ForgotPasswordResponse(
            success=True,
            message=f"If the email exists, a password reset has been sent via {notification_type}"
        )
        
    except Exception:
        return ForgotPasswordResponse(
            success=False,
            message="Failed to process forgot password request"
        )


"""
Usage Examples:

1. Email-only endpoint:
   POST /auth/forgot-password/email
   {"email": "user@example.com"}

2. SMS-only endpoint:
   POST /auth/forgot-password/sms
   {"email": "user@example.com"}

3. Flexible endpoint:
   POST /auth/forgot-password?notification_type=email
   {"email": "user@example.com"}
   
   POST /auth/forgot-password?notification_type=sms
   {"email": "user@example.com"}

Key Benefits of This Design:

1. **Extensibility**: Easy to add new notification providers (push notifications, 
   WhatsApp, etc.) by implementing the NotificationService interface

2. **Testability**: Each component can be tested in isolation with mock dependencies

3. **Configuration**: Different providers can have different configurations

4. **Flexibility**: Can easily switch between providers or support multiple 
   notification methods based on user preferences

5. **Separation of Concerns**: Notification logic is separate from business logic

6. **Dependency Injection**: FastAPI's dependency system makes it easy to 
   configure and inject the right services
"""