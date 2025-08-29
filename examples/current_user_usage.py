"""
Example usage of CurrentUserService for protected endpoints.

This shows how to use the CurrentUserService in a FastAPI endpoint
to get the authenticated user from JWT tokens.
"""

from fastapi import APIRouter, Depends, Request

from app.models.user import User
from app.services.current_user_service import CurrentUserService

# Example router for protected endpoints
router = APIRouter(tags=["Protected"])


@router.get("/me", summary="Get current user profile")
async def get_current_user_profile(
    request: Request,
    current_user_service: CurrentUserService = Depends(CurrentUserService),
):
    """Get the current authenticated user's profile."""
    current_user = await current_user_service.get_current_user(request)
    
    return {
        "success": True,
        "message": "User profile retrieved successfully",
        "user": {
            "id": str(current_user.id),
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "dob": current_user.dob.isoformat(),
        },
    }


@router.get("/profile", summary="Alternative way to get current user")
async def get_profile(
    current_user: User = Depends(
        lambda request, service=Depends(CurrentUserService): service.get_current_user(
            request
        )
    ),
):
    """Alternative approach using dependency injection directly."""
    return {
        "success": True,
        "user": {
            "email": current_user.email,
            "name": f"{current_user.first_name} {current_user.last_name}",
        },
    }


# To use this router, add it to your main FastAPI app:
# app.include_router(router, prefix="/api")

# Example API calls:
# GET /api/me
# Headers: Authorization: Bearer <your-jwt-token>
#
# GET /api/profile  
# Headers: Authorization: Bearer <your-jwt-token>