from fastapi import Depends, HTTPException, status, Request

from app.models.user import User
from app.services.session_provider import SessionProvider
from app.services.token_session_provider import TokenSessionProvider
from app.services.user_service import UserService


class CurrentUserService:
    """Service for getting the current authenticated user."""

    def __init__(
        self,
        user_service: UserService = Depends(UserService),
        session_provider: SessionProvider = Depends(TokenSessionProvider),
    ):
        self._user_service = user_service
        self._session_provider = session_provider

    async def get_current_user(self, request: Request) -> User:
        """Get the current authenticated user from the request.

        Args:
            request: FastAPI request object

        Returns:
            User model of the authenticated user

        Raises:
            HTTPException: If user is not authenticated or not found
        """
        # Get session data from provider
        session_data = await self._session_provider.get_session(request)

        # Extract user identifier from session
        user_email = session_data.get("email")
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User email not found in session",
            )

        # Get user from service
        user = await self._user_service.find_by_email(user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        return user
