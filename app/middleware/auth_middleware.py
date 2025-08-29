from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, status

from app.utils.jwt_utils import get_user_id_from_token


class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware to validate JWT tokens on protected routes"""
    
    # Routes that don't require authentication
    EXEMPT_PATHS = {
        "/",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/login",
        "/register",
        "/health",
        "/public"  # Added for testing
    }
    
    def __init__(self, app, exempt_paths: set = None):
        super().__init__(app)
        if exempt_paths:
            self.EXEMPT_PATHS.update(exempt_paths)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip authentication for exempt paths
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)
        
        # Skip authentication for OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Check for Authorization header
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Extract token from "Bearer <token>" format
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Validate token and extract user ID
        try:
            user_id = get_user_id_from_token(token)
            # Add user_id to request state for use in route handlers
            request.state.user_id = user_id
        except HTTPException:
            # Re-raise HTTP exceptions from token validation
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        response = await call_next(request)
        return response