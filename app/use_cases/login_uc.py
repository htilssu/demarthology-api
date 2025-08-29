from fastapi import Depends, HTTPException, status
from starlette.responses import Response

from app.repositories.user_repository import UserRepository
from app.schemas.login_request import LoginRequest
from app.use_cases.usecase import UseCase
from app.utils.password import verify_password
from app.utils.jwt_token import generate_token


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

        # Prepare user data for token
        user_data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        
        # Generate JWT token
        access_token = generate_token(user_data)

        # Return success response with token
        return {
            "success": True,
            "message": "Login successful",
            "user": user_data,
            "access_token": access_token,
            "token_type": "bearer"
        }
