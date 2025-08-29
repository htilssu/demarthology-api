from datetime import timedelta
from fastapi import Depends, HTTPException, status
from starlette.responses import JSONResponse

from app.configs.setting import setting
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.login_request import LoginRequest
from app.use_cases.usecase import UseCase
from app.utils.jwt_utils import create_access_token


class LoginUC(UseCase):
    def __init__(self):
        pass

    async def action(self, *args, **kwargs):
        data: LoginRequest = args[0]
        
        # Initialize repository
        user_repo = UserRepository()
        
        # Find user by email
        try:
            # Using find_one method to search by email
            user = await User.find_one(User.email == data.username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # In a real application, you should hash and verify passwords
        # For now, we'll do a simple comparison
        if user.password != data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=setting.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }

