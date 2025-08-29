from typing import Any
from fastapi import HTTPException, status

from app.models.user import User
from app.utils.permission import Permission, PermissionContext


async def authorize[T](
    permission: Permission[T], context: PermissionContext[T]
) -> None:
    """Authorize access based on permission and context.

    Args:
        permission: The permission instance to check
        context: The permission context containing user and optional resource

    Raises:
        HTTPException: If permission is not granted (403 Forbidden)
    """
    if not await permission.authorize(context):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )
