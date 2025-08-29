from typing import Dict, Any

from fastapi import Request, HTTPException, status

from app.services.session_provider import SessionProvider
from app.utils.jwt import JWTUtils


class TokenSessionProvider(SessionProvider):
    """Token-based session provider using JWT tokens."""

    async def get_session(self, request: Request) -> Dict[str, Any]:
        """Get session data from JWT token in Authorization header.

        Args:
            request: FastAPI request object

        Returns:
            Dict containing decoded token payload

        Raises:
            HTTPException: If token is missing, invalid, or expired
        """
        # Get Authorization header
        authorization: str = request.headers.get("Authorization")

        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
            )

        # Check if it starts with "Bearer "
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header must start with 'Bearer '",
            )

        # Extract token
        token = authorization.split(" ")[1]

        # Decode and validate token
        payload = JWTUtils.decode_access_token(token)

        return payload
