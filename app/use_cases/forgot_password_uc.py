from fastapi import Depends, HTTPException, status

from app.schemas.auth_responses import ForgotPasswordResponse
from app.schemas.forgot_password_request import ForgotPasswordRequest
from app.services.forgot_password_service import ForgotPasswordService
from app.use_cases.usecase import UseCase


class ForgotPasswordUC(UseCase):
    """Use case for handling forgot password requests."""

    def __init__(self, forgot_password_service: ForgotPasswordService = Depends(ForgotPasswordService)):
        self._forgot_password_service = forgot_password_service

    async def action(self, data: ForgotPasswordRequest) -> ForgotPasswordResponse:
        """Process forgot password request."""
        try:
            # Send forgot password notification
            await self._forgot_password_service.send_forgot_password_notification(
                email=str(data.email),
                notification_type="email"
            )

            # Always return success for security (don't reveal if email exists)
            return ForgotPasswordResponse(
                success=True,
                message="If the email exists, a password reset link has been sent",
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process forgot password request",
            )
