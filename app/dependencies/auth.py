from fastapi import Depends, Request, HTTPException, status
from app.models.user import User
from app.repositories.user_repository import UserRepository


async def get_current_user(request: Request) -> User:
    """Dependency to get the current authenticated user"""
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    
    user_repo = UserRepository()
    user_repo.document_class = User
    try:
        user = await user_repo.get(user_id)
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )