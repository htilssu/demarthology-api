from contextvars import ContextVar
from fastapi import Request
from app.application.common.ports.identity_provider import IdentityProvider

# Context variable to store the current request
_request_context: ContextVar[Request] = ContextVar('request_context')


class FastAPIIdentityProvider(IdentityProvider):
    """FastAPI implementation of IdentityProvider"""
    
    async def get_current_user_id(self) -> str:
        """Get the current user ID from the request context"""
        request = _request_context.get(None)
        if not request:
            raise ValueError("No request context available")
        
        user_id = getattr(request.state, 'user_id', None)
        if not user_id:
            raise ValueError("No user ID in request state")
        
        return user_id


def set_request_context(request: Request) -> None:
    """Set the request context for the current operation"""
    _request_context.set(request)