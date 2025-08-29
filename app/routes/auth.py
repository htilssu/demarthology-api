from fastapi import APIRouter, Depends

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
