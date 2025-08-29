import logging
from app.application.common.ports.access_revoker import AccessRevoker

log = logging.getLogger(__name__)


class JWTAccessRevoker(AccessRevoker):
    """JWT implementation of AccessRevoker"""
    
    async def remove_all_user_access(self, user_id: str) -> None:
        """Remove all access for a user"""
        # In a JWT-based system, we typically can't revoke tokens immediately
        # This could be implemented by maintaining a blacklist or by reducing token expiry
        # For now, we'll just log the action
        log.info(f"Access revoked for user ID: {user_id}")
        # TODO: Implement token blacklist or force re-authentication