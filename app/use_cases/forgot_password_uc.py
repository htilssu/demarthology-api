from fastapi import Depends, HTTPException, status

from app.schemas.auth_responses import ForgotPasswordResponse
from app.schemas.forgot_password_request import ForgotPasswordRequest
from app.services.user_service import UserService
from app.use_cases.usecase import UseCase
from app.utils.jwt import JWTUtils


class ForgotPasswordUC(UseCase):
    """Use case for handling forgot password requests."""

    def __init__(self, user_service: UserService = Depends(UserService)):
        self._user_service = user_service

    async def action(self, data: ForgotPasswordRequest) -> ForgotPasswordResponse:
        """Process forgot password request."""
        try:
            # Check if user exists
            user_exists = await self._user_service.check_user_exist(data.email)

            # Always return success for security (don't reveal if email exists)
            # In production, you would send email here if user exists
            if user_exists:
                # Generate reset token
                reset_token = JWTUtils.create_reset_token(data.email)
                # TODO: Send email with reset link containing the token
                # For now, just log the token (remove in production)
                print(f"Reset token for {data.email}: {reset_token}")

            return ForgotPasswordResponse(
                success=True,
                message="If the email exists, a password reset link has been sent",
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process forgot password request",
            )
