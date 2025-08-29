from fastapi import Request, HTTPException, status
from app.domain.entities.user import User
from app.application.common.services.current_user_service import CurrentUserService
from app.application.common.exceptions.authorization import AuthorizationError
from app.infrastructure.adapters.fastapi_identity_provider import FastAPIIdentityProvider, set_request_context
from app.infrastructure.adapters.mongo_user_command_gateway import MongoUserCommandGateway
from app.infrastructure.adapters.jwt_access_revoker import JWTAccessRevoker


async def get_current_user(request: Request) -> User:
    """Dependency to get the current authenticated user"""
    # Set request context for the identity provider
    set_request_context(request)
    
    # Create service with adapters
    identity_provider = FastAPIIdentityProvider()
    user_command_gateway = MongoUserCommandGateway()
    access_revoker = JWTAccessRevoker()
    
    current_user_service = CurrentUserService(
        identity_provider=identity_provider,
        user_command_gateway=user_command_gateway,
        access_revoker=access_revoker
    )
    
    try:
        user = await current_user_service.get_current_user()
        return user
    except AuthorizationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not authenticate user"
        )