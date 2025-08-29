from typing import Any, List
from fastapi import HTTPException, status

from app.models.user import User
from app.utils.permission import Permission


async def check_permission(
    user: User, permission: Permission, resource: Any = None
) -> bool:
    """Check if user has the specified permission.

    Args:
        user: The user to check permissions for
        permission: The permission instance to check
        resource: Optional resource being accessed

    Returns:
        True if user has permission, False otherwise
    """
    return await permission.authorize(user, resource)


async def require_permission(
    user: User, permission: Permission, resource: Any = None
) -> None:
    """Require that user has the specified permission.

    Args:
        user: The user to check permissions for
        permission: The permission instance to check
        resource: Optional resource being accessed

    Raises:
        HTTPException: If user doesn't have permission (403 Forbidden)
    """
    if not await check_permission(user, permission, resource):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )


async def check_any_permission(
    user: User, permissions: List[Permission], resource: Any = None
) -> bool:
    """Check if user has any of the specified permissions.

    Args:
        user: The user to check permissions for
        permissions: List of permission instances to check
        resource: Optional resource being accessed

    Returns:
        True if user has at least one permission, False otherwise
    """
    for permission in permissions:
        if await permission.authorize(user, resource):
            return True
    return False


async def check_all_permissions(
    user: User, permissions: List[Permission], resource: Any = None
) -> bool:
    """Check if user has all of the specified permissions.

    Args:
        user: The user to check permissions for
        permissions: List of permission instances to check
        resource: Optional resource being accessed

    Returns:
        True if user has all permissions, False otherwise
    """
    for permission in permissions:
        if not await permission.authorize(user, resource):
            return False
    return True


async def require_any_permission(
    user: User, permissions: List[Permission], resource: Any = None
) -> None:
    """Require that user has any of the specified permissions.

    Args:
        user: The user to check permissions for
        permissions: List of permission instances to check
        resource: Optional resource being accessed

    Raises:
        HTTPException: If user doesn't have any permission (403 Forbidden)
    """
    if not await check_any_permission(user, permissions, resource):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )


async def require_all_permissions(
    user: User, permissions: List[Permission], resource: Any = None
) -> None:
    """Require that user has all of the specified permissions.

    Args:
        user: The user to check permissions for
        permissions: List of permission instances to check
        resource: Optional resource being accessed

    Raises:
        HTTPException: If user doesn't have all permissions (403 Forbidden)
    """
    if not await check_all_permissions(user, permissions, resource):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )
