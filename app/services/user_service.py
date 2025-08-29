from fastapi import Depends, HTTPException, status

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self._user_repository = user_repository

    async def check_user_exist(self, email: str) -> bool:
        """Check if a user exists by email address."""
        try:
            existing_user = await self._user_repository.find_by_email(email)
            return existing_user is not None
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error checking user existence: {str(e)}",
            )

    async def save_user(self, user: User) -> User:
        """Save a user to the database."""
        try:
            await user.create()
            return user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving user: {str(e)}",
            )

    async def find_by_email(self, email: str) -> User | None:
        """Find a user by email address."""
        try:
            return await self._user_repository.find_by_email(email)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error finding user: {str(e)}",
            )
