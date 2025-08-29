from fastapi import Depends, HTTPException, status

from app.models.user import User
from app.schemas.login_response import UserInfo
from app.schemas.register_request import RegisterRequest
from app.schemas.register_response import RegisterResponse
from app.services.role_service import RoleService
from app.services.user_service import UserService
from app.use_cases.usecase import UseCase
from app.utils.password import hash_password


class RegisterUC(UseCase):
    def __init__(
        self,
        user_service: UserService = Depends(UserService),
        role_service: RoleService = Depends(RoleService),
    ):
        self._user_service = user_service
        self._role_service = role_service

    async def action(self, *args, **kwargs):
        data: RegisterRequest = args[0]

        # Check if user already exists
        if await self._user_service.check_user_exist(str(data.email)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        # Get or create the role
        role = await self._role_service.get_role_by_name(data.role)
        if not role:
            # If role doesn't exist, use default 'user' role
            role = await self._role_service.get_or_create_default_role()

        # Hash the password
        hashed_password = hash_password(data.password)

        # Create new user
        new_user = User(
            email=str(data.email),
            password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
            dob=data.dob,
            role=role,
        )

        # Save user to database through service
        saved_user = await self._user_service.save_user(new_user)

        # Fetch role name for response
        role_name = None
        if saved_user.role:
            await saved_user.fetch_link(User.role)
            role_name = saved_user.role.name if saved_user.role else "user"

        # Return success response
        user_info = UserInfo(
            email=saved_user.email,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
            role=role_name,  # Include role name in response
        )
        return RegisterResponse(success=True, message="Registration successful", user=user_info)
