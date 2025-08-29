from fastapi import Depends, HTTPException, status
from starlette.responses import Response

from app.repositories.user_repository import UserRepository
from app.schemas.login_request import LoginRequest
from app.use_cases.usecase import UseCase
from app.utils.password import verify_password


class LoginUC(UseCase):
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self._user_repository = user_repository

    async def action(self, *args, **kwargs):
        data: LoginRequest = args[0]

        # Find user by email (username field maps to email)
        user = await self._user_repository.find_by_email(data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Verify password
        if not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Return success response
        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }
