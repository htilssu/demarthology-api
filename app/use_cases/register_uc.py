from datetime import timedelta
from fastapi import HTTPException, status

from app.configs.setting import setting
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.register_request import RegisterRequest
from app.use_cases.usecase import UseCase
from app.utils.jwt_utils import create_access_token
from app.utils.password_utils import hash_password


class RegisterUC(UseCase):
    def __init__(self):
        pass

    async def action(self, *args, **kwargs):
        data: RegisterRequest = args[0]
        
        # Check if user already exists
        existing_user = await User.find_one(User.email == data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Hash password
        hashed_password = hash_password(data.password)
        
        # Create new user
        new_user = User(
            email=data.email,
            password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
            dob=data.dob
        )
        
        # Save user to database
        try:
            await new_user.insert()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=setting.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(new_user.id)}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(new_user.id),
                "email": new_user.email,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name
            }
        }