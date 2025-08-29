from fastapi import Depends, Request

from app.schemas.auth_responses import LogoutResponse
from app.services.current_user_service import CurrentUserService
from app.use_cases.usecase import UseCase


class LogoutUC(UseCase):
    """Use case for handling logout requests."""

    def __init__(self, current_user_service: CurrentUserService = Depends(CurrentUserService)):
        self._current_user_service = current_user_service

    async def action(self, request: Request) -> LogoutResponse:
        """Process logout request."""
        # For JWT tokens, logout is typically handled client-side
        # by removing the token from storage.
        # We could implement token blacklisting here if needed.

        # Validate that the user is authenticated (has valid token)
        await self._current_user_service.get_current_user(request)

        return LogoutResponse(success=True, message="Logged out successfully")
