from fastapi import Depends, HTTPException, status

from app.models.user import User
from app.services.user_service import UserService
from app.schemas.register_request import RegisterRequest
from app.schemas.register_response import RegisterResponse
from app.schemas.login_response import UserInfo
from app.use_cases.usecase import UseCase
from app.utils.password import hash_password


class RegisterUC(UseCase):
    def __init__(self, user_service: UserService = Depends(UserService)):
        self._user_service = user_service

    async def action(self, *args, **kwargs):
        data: RegisterRequest = args[0]

        # Check if passwords match
        if data.password != data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
            )

        # Check if user already exists
        if await self._user_service.check_user_exist(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        # Hash the password
        hashed_password = hash_password(data.password)

        # Create new user
        new_user = User(
            email=data.email,
            password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
            dob=data.dob,
        )

        # Save user to database through service
        saved_user = await self._user_service.save_user(new_user)

        # Return success response
        user_info = UserInfo(
            email=saved_user.email,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
        )
        return RegisterResponse(
            success=True, message="Registration successful", user=user_info
        )
