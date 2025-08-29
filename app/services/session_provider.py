from abc import ABC, abstractmethod
from typing import Dict, Any

from fastapi import Request


class SessionProvider(ABC):
    """Abstract base class for session providers."""

    @abstractmethod
    async def get_session(self, request: Request) -> Dict[str, Any]:
        """Get session data from the request.

        Args:
            request: FastAPI request object

        Returns:
            Dict containing session data (e.g., user_id, email, etc.)

        Raises:
            HTTPException: If session is invalid or missing
        """
        pass
