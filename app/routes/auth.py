from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.login_request import LoginRequest
from app.use_cases.login_uc import LoginUC
from app.use_cases.usecase import UseCase

router = APIRouter(tags=["Authentication"])


@router.post("/login", summary="Đăng nhập")
async def login(data: LoginRequest, uc: UseCase = Depends(LoginUC)):
    return await uc.action(data)


@router.post("/register", summary="Đăng ký")
async def register(data: LoginRequest):
    pass


@router.get("/me", summary="Get current user profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "dob": current_user.dob
    }
