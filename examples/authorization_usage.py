"""
Example usage of the new role-based authorization system.

This example shows how to use the authorization utilities and permission classes
in FastAPI routes to protect endpoints based on user roles and permissions.
"""

from fastapi import Depends, Request
from app.models.user import User
from app.services.current_user_service import CurrentUserService
from app.utils import (
    AuthorizeUtil,
    AdminPermission,
    UserPermission,
    RolePermission,
    SelfOrAdminPermission,
)


# Example 1: Protecting a route with admin-only access
async def admin_only_endpoint(
    request: Request,
    current_user_service: CurrentUserService = Depends(CurrentUserService),
):
    """Example endpoint that requires admin role."""
    # Get current user
    current_user = await current_user_service.get_current_user(request)
    
    # Check admin permission
    admin_permission = AdminPermission()
    await AuthorizeUtil.require_permission(current_user, admin_permission)
    
    return {"message": "Welcome, admin!", "user": current_user.email}


# Example 2: Protecting a route with multiple role access
async def moderator_or_admin_endpoint(
    request: Request,
    current_user_service: CurrentUserService = Depends(CurrentUserService),
):
    """Example endpoint that requires moderator or admin role."""
    # Get current user
    current_user = await current_user_service.get_current_user(request)
    
    # Check permissions (moderator OR admin)
    permissions = [
        RolePermission("moderator"),
        RolePermission("admin"),
    ]
    await AuthorizeUtil.require_any_permission(current_user, permissions)
    
    return {"message": "Welcome, moderator or admin!", "user": current_user.email}


# Example 3: Self-or-admin access pattern
async def get_user_profile(
    user_id: str,
    request: Request,
    current_user_service: CurrentUserService = Depends(CurrentUserService),
):
    """Example endpoint where users can access their own profile or admins can access any."""
    # Get current user
    current_user = await current_user_service.get_current_user(request)
    
    # Create a mock resource representing the target user
    target_resource = type('UserResource', (), {'user_id': user_id})()
    
    # Check self-or-admin permission
    permission = SelfOrAdminPermission()
    await AuthorizeUtil.require_permission(current_user, permission, target_resource)
    
    return {"message": f"Profile for user {user_id}", "accessed_by": current_user.email}


# Example 4: Basic user access (any authenticated user)
async def user_dashboard(
    request: Request,
    current_user_service: CurrentUserService = Depends(CurrentUserService),
):
    """Example endpoint accessible by any authenticated user."""
    # Get current user
    current_user = await current_user_service.get_current_user(request)
    
    # Check basic user permission
    user_permission = UserPermission()
    await AuthorizeUtil.require_permission(current_user, user_permission)
    
    return {"message": "Welcome to your dashboard!", "user": current_user.email}


# Example 5: Conditional logic based on permissions
async def conditional_access_endpoint(
    request: Request,
    current_user_service: CurrentUserService = Depends(CurrentUserService),
):
    """Example endpoint with conditional logic based on user permissions."""
    # Get current user
    current_user = await current_user_service.get_current_user(request)
    
    # Check if user has admin access
    admin_permission = AdminPermission()
    is_admin = await AuthorizeUtil.check_permission(current_user, admin_permission)
    
    if is_admin:
        # Admin gets full data
        return {
            "message": "Full admin data",
            "user": current_user.email,
            "role": current_user.role,
            "admin_data": {"sensitive": "information"},
        }
    else:
        # Regular users get limited data
        user_permission = UserPermission()
        await AuthorizeUtil.require_permission(current_user, user_permission)
        
        return {
            "message": "Limited user data",
            "user": current_user.email,
        }


# Example 6: Custom permission class
class OwnerPermission:
    """Custom permission that checks resource ownership."""
    
    def __init__(self, resource_owner_email: str):
        self.resource_owner_email = resource_owner_email
    
    async def authorize(self, user: User, resource=None) -> bool:
        """Check if user owns the resource or is admin."""
        # Admin can access everything
        if user.role == "admin":
            return True
        
        # User can access if they own the resource
        return user.email == self.resource_owner_email


async def custom_permission_endpoint(
    resource_owner: str,
    request: Request,
    current_user_service: CurrentUserService = Depends(CurrentUserService),
):
    """Example endpoint using a custom permission class."""
    # Get current user
    current_user = await current_user_service.get_current_user(request)
    
    # Use custom permission
    owner_permission = OwnerPermission(resource_owner)
    await AuthorizeUtil.require_permission(current_user, owner_permission)
    
    return {
        "message": f"Access granted to resource owned by {resource_owner}",
        "accessed_by": current_user.email,
    }


# Example usage in FastAPI app:
"""
from fastapi import FastAPI

app = FastAPI()

# Register the protected routes
app.get("/admin-only")(admin_only_endpoint)
app.get("/moderator-or-admin")(moderator_or_admin_endpoint)
app.get("/user/{user_id}/profile")(get_user_profile)
app.get("/dashboard")(user_dashboard)
app.get("/conditional")(conditional_access_endpoint)
app.get("/custom/{resource_owner}")(custom_permission_endpoint)
"""