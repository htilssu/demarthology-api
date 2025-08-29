"""
Example protected route that uses CurrentUserService.

This example demonstrates how to create a protected API endpoint that requires
JWT authentication and returns user information.
"""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request, status

from app.errors.unauthorized import UnauthorizedException
from app.services.current_user_service import CurrentUserService

# Create router for example endpoints
router = APIRouter(prefix="/api", tags=["Example Protected Routes"])

# Initialize CurrentUserService
current_user_service = CurrentUserService()


@router.get("/profile", summary="Get user profile (requires authentication)")
async def get_user_profile(request: Request) -> Dict[str, Any]:
    """
    Get current user profile information.

    Requires valid JWT token in Authorization header:
    Authorization: Bearer <your_jwt_token>

    Returns:
        Dict containing user profile information

    Raises:
        HTTPException: 401 if authentication fails
    """
    try:
        # Get current user from JWT token
        user_data = current_user_service.get_current_user(request)

        return {
            "success": True,
            "message": "Profile retrieved successfully",
            "profile": {
                "email": user_data["email"],
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "full_name": f"{user_data['first_name']} {user_data['last_name']}",
            },
        }
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/protected", summary="Protected endpoint example")
async def protected_endpoint(request: Request) -> Dict[str, Any]:
    """
    Example of a protected endpoint that requires authentication.

    Returns:
        Dict with personalized greeting for authenticated user
    """
    try:
        user_data = current_user_service.get_current_user(request)

        return {
            "message": f"Hello {user_data['first_name']}! This is a protected endpoint.",
            "user_email": user_data["email"],
            "access_granted": True,
            "timestamp": "2024-01-01T00:00:00Z",  # In real app, use datetime.utcnow()
        }
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


# To use this in your main.py, add:
"""
from examples.protected_routes_example import router as protected_router

app.include_router(protected_router)
"""

# Example requests:
"""
# 1. First login to get a token:
POST /login
{
    "email": "user@example.com",
    "password": "yourpassword"
}

# Response:
{
    "success": true,
    "message": "Login successful",
    "user": {...},
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}

# 2. Use the token to access protected endpoints:
GET /api/profile
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# 3. Or access other protected endpoints:
GET /api/protected
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
"""
