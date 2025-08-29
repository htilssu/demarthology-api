from app.models.user import User
from app.utils.authorize import Permission, PermissionContext


class UploadManageContext(PermissionContext):
    user: User


class CanUploadPermission(UploadManageContext):
    """Permission schema for user uploading."""

    async def authorize(self, context: UploadManageContext) -> bool:
        # TODO:implement

        return True
