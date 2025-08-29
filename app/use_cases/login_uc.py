from fastapi import Depends, HTTPException, status
from starlette.responses import Response

from app.services.user_service import UserService
from app.schemas.login_request import LoginRequest
from app.schemas.login_response import LoginResponse, UserInfo
from app.use_cases.usecase import UseCase
from app.utils.password import verify_password
from app.utils.jwt import JWTUtils


class LoginUC(UseCase):
    def __init__(self, user_service: UserService = Depends(UserService)):
        self._user_service = user_service

    async def action(self, *args, **kwargs):
        data: LoginRequest = args[0]

        # Find user by email (username field maps to email)
        user = await self._user_service.find_by_email(data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # Verify password
        if not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # Create access token
        token_data = {"email": user.email, "user_id": str(user.id)}
        access_token = JWTUtils.create_access_token(token_data)

        # Return success response with token
        user_info = UserInfo(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,  # Include role in response
        )
        return LoginResponse(
            success=True,
            message="Login successful",
            user=user_info,
            access_token=access_token,
        )
