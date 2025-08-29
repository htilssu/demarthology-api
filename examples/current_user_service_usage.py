"""
Example usage of CurrentUserService in FastAPI routes.

This file demonstrates how to use the CurrentUserService to protect API endpoints
and get current user information from JWT tokens.
"""

from typing import Any, Dict

from fastapi import Depends, HTTPException, Request, status

from app.errors.unauthorized import UnauthorizedException
from app.services.current_user_service import CurrentUserService


def get_current_user_service() -> CurrentUserService:
    """Dependency to provide CurrentUserService instance."""
    return CurrentUserService()


def get_current_user(request: Request, user_service: CurrentUserService = Depends(get_current_user_service)) -> Dict[str, Any]:
    """
    FastAPI dependency to get current authenticated user.

    This can be used as a dependency in FastAPI routes to ensure the user
    is authenticated and to get their information.

    Args:
        request (Request): FastAPI request object
        user_service (CurrentUserService): CurrentUserService instance

    Returns:
        Dict[str, Any]: Current user data from JWT token

    Raises:
        HTTPException: 401 if authentication fails
    """
    try:
        return user_service.get_current_user(request)
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


# Example usage in routes:
"""
from fastapi import APIRouter, Depends
from .auth_dependencies import get_current_user

router = APIRouter()

@router.get("/profile")
async def get_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "message": "User profile",
        "user": current_user
    }

@router.get("/protected")
async def protected_endpoint(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "message": f"Hello {current_user['first_name']}!",
        "access_granted": True
    }
"""
