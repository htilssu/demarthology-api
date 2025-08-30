# Forgot Password Notification Service

This document explains how to use and extend the forgot password notification service implementation.

## Overview

The forgot password functionality is implemented using an abstract notification service pattern that allows for multiple notification methods (email, SMS, push notifications, etc.) to be easily integrated and swapped.

## Architecture

```
ForgotPasswordUC (Use Case)
    ↓
ForgotPasswordService (Business Logic)
    ↓
NotificationService (Abstract Interface)
    ↓
EmailNotificationService | SMSNotificationService | CustomNotificationService
```

## Core Components

### 1. NotificationService (Abstract Base Class)

```python
from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    async def send_forgot_password(self, email: str, reset_token: str, **kwargs) -> bool:
        pass
```

### 2. Concrete Implementations

#### EmailNotificationService
```python
email_service = EmailNotificationService({
    "host": "smtp.gmail.com",
    "port": 587,
    "username": "noreply@yourapp.com",
    "password": "your-password",
    "use_tls": True
})
```

#### SMSNotificationService
```python
sms_service = SMSNotificationService({
    "provider": "twilio",
    "account_sid": "your-sid",
    "auth_token": "your-token",
    "from_number": "+1234567890"
})
```

### 3. ForgotPasswordService

```python
service = ForgotPasswordService(
    user_service=user_service,
    notification_service=email_service  # or sms_service
)

await service.send_forgot_password_notification(
    email="user@example.com",
    subject="Reset Your Password",
    reset_link="https://app.com/reset?token=xyz"
)
```

## Usage Examples

### Basic Email Notification

```python
from app.services.notification_service import EmailNotificationService
from app.services.forgot_password_service import ForgotPasswordService
from app.services.user_service import UserService

# Configure email service
email_config = {
    "host": "smtp.gmail.com",
    "port": 587,
    "username": "noreply@yourapp.com",
    "password": "your-app-password"
}
email_service = EmailNotificationService(email_config)

# Create forgot password service
user_service = UserService()
forgot_service = ForgotPasswordService(
    user_service=user_service,
    notification_service=email_service
)

# Send notification
await forgot_service.send_forgot_password_notification(
    email="user@example.com",
    subject="Password Reset Request",
    reset_link="https://yourapp.com/reset?token=abc123"
)
```

### Basic SMS Notification

```python
from app.services.notification_service import SMSNotificationService

# Configure SMS service
sms_config = {
    "provider": "twilio",
    "account_sid": "your-twilio-sid",
    "auth_token": "your-twilio-token",
    "from_number": "+1234567890"
}
sms_service = SMSNotificationService(sms_config)

# Create forgot password service
forgot_service = ForgotPasswordService(
    user_service=user_service,
    notification_service=sms_service
)

# Send notification
await forgot_service.send_forgot_password_notification(
    email="user@example.com",
    phone_number="+1987654321",
    message="Your password reset code: 123456"
)
```

## Extending the System

### Creating a Custom Notification Service

To add a new notification method (e.g., push notifications, WhatsApp, Slack), implement the `NotificationService` interface:

```python
from app.services.notification_service import NotificationService

class PushNotificationService(NotificationService):
    def __init__(self, push_config: dict):
        self.push_config = push_config
    
    async def send_forgot_password(self, email: str, reset_token: str, **kwargs) -> bool:
        try:
            # Look up user's device tokens by email
            device_tokens = await self.get_user_device_tokens(email)
            
            # Create push notification payload
            payload = {
                "title": "Password Reset",
                "body": "Tap to reset your password",
                "data": {
                    "reset_token": reset_token,
                    "action": "forgot_password"
                }
            }
            
            # Send push notification
            success = await self.send_push_notification(device_tokens, payload)
            return success
            
        except Exception as e:
            print(f"Failed to send push notification: {str(e)}")
            return False
    
    async def get_user_device_tokens(self, email: str):
        # Implement device token lookup
        pass
    
    async def send_push_notification(self, tokens, payload):
        # Implement actual push notification sending
        pass
```

### Using Custom Notification Service

```python
# Configure push service
push_config = {
    "firebase_server_key": "your-firebase-key",
    "app_id": "your-app-id"
}
push_service = PushNotificationService(push_config)

# Create forgot password service
forgot_service = ForgotPasswordService(
    user_service=user_service,
    notification_service=push_service
)

# Send notification
await forgot_service.send_forgot_password_notification(
    email="user@example.com"
)
```

### Multi-Channel Notifications

You can also create a composite service that sends notifications through multiple channels:

```python
class MultiChannelNotificationService(NotificationService):
    def __init__(self, services: list[NotificationService]):
        self.services = services
    
    async def send_forgot_password(self, email: str, reset_token: str, **kwargs) -> bool:
        results = []
        for service in self.services:
            try:
                result = await service.send_forgot_password(email, reset_token, **kwargs)
                results.append(result)
            except Exception:
                results.append(False)
        
        # Return True if at least one service succeeded
        return any(results)

# Usage
email_service = EmailNotificationService(email_config)
sms_service = SMSNotificationService(sms_config)
multi_service = MultiChannelNotificationService([email_service, sms_service])

forgot_service = ForgotPasswordService(
    user_service=user_service,
    notification_service=multi_service
)
```

## Configuration

### Environment Variables

For production use, store sensitive configuration in environment variables:

```python
import os
from app.services.notification_service import EmailNotificationService

email_config = {
    "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
    "port": int(os.getenv("SMTP_PORT", "587")),
    "username": os.getenv("SMTP_USERNAME"),
    "password": os.getenv("SMTP_PASSWORD"),
    "use_tls": os.getenv("SMTP_USE_TLS", "true").lower() == "true"
}

email_service = EmailNotificationService(email_config)
```

### FastAPI Dependencies

Use FastAPI's dependency injection system for clean configuration:

```python
from fastapi import Depends

def get_email_service() -> EmailNotificationService:
    return EmailNotificationService(email_config)

def get_forgot_password_service(
    user_service: UserService = Depends(UserService),
    notification_service: EmailNotificationService = Depends(get_email_service)
) -> ForgotPasswordService:
    return ForgotPasswordService(user_service, notification_service)

@app.post("/auth/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    service: ForgotPasswordService = Depends(get_forgot_password_service)
):
    await service.send_forgot_password_notification(str(request.email))
    return {"success": True}
```

## Security Considerations

1. **Don't Leak User Existence**: The service always returns success, regardless of whether the user exists
2. **Token Expiration**: Reset tokens expire in 15 minutes by default
3. **Rate Limiting**: Consider implementing rate limiting on forgot password endpoints
4. **Secure Token Generation**: Uses JWT with proper expiration times
5. **Configuration Security**: Store sensitive configuration (API keys, passwords) in environment variables

## Testing

The system includes comprehensive tests for all components:

```bash
# Run all forgot password tests
python -m pytest tests/test_notification_service.py tests/test_forgot_password_service.py tests/test_forgot_password_uc.py -v

# Run specific test
python -m pytest tests/test_notification_service.py::TestEmailNotificationService -v
```

Mock services for testing:

```python
from unittest.mock import Mock, AsyncMock

# Mock notification service
mock_notification = Mock()
mock_notification.send_forgot_password = AsyncMock(return_value=True)

# Mock user service
mock_user_service = Mock()
mock_user_service.check_user_exist = AsyncMock(return_value=True)

# Test service
service = ForgotPasswordService(
    user_service=mock_user_service,
    notification_service=mock_notification
)
```

## Best Practices

1. **Use Abstract Interfaces**: Always program against the `NotificationService` interface
2. **Handle Failures Gracefully**: Notification failures shouldn't crash the application
3. **Log Appropriately**: Log errors but don't expose sensitive information
4. **Configuration Validation**: Validate configuration parameters on service initialization
5. **Async/Await**: Use async methods for all I/O operations
6. **Dependency Injection**: Use FastAPI's dependency system for clean architecture
7. **Error Handling**: Implement proper exception handling in custom services
8. **Testing**: Write comprehensive tests for custom notification services