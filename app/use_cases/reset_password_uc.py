from fastapi import Depends, HTTPException, status

from app.schemas.auth_responses import ResetPasswordResponse
from app.schemas.reset_password_request import ResetPasswordRequest
from app.services.user_service import UserService
from app.use_cases.usecase import UseCase
from app.utils.jwt import JWTUtils
from app.utils.password import PasswordUtils


class ResetPasswordUC(UseCase):
    """Use case for handling password reset requests."""

    def __init__(self, user_service: UserService = Depends(UserService)):
        self._user_service = user_service

    async def action(self, data: ResetPasswordRequest) -> ResetPasswordResponse:
        """Process password reset request."""
        try:
            # Decode and validate reset token
            email = JWTUtils.decode_reset_token(data.token)

            if not email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid reset token",
                )

            # Find user by email
            user = await self._user_service.find_by_email(email)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            # Hash new password
            hashed_password = PasswordUtils.hash_password(data.new_password)

            # Update user password
            user.password = hashed_password
            await self._user_service.save_user(user)

            return ResetPasswordResponse(success=True, message="Password has been reset successfully")

        except HTTPException:
            # Re-raise HTTP exceptions as they contain proper error messages
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to reset password",
            )
