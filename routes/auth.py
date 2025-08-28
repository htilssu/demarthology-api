from fastapi import APIRouter, Depends

from schemas.login_request import LoginRequest
from use_cases.login_uc import LoginUC
from use_cases.usecase import UseCase

router = APIRouter(tags=["Authentication"])


@router.post("/login", summary="Đăng nhập")
async def login(data: LoginRequest, uc: UseCase = Depends(LoginUC)):
    await uc.action(data)


@router.post("/register", summary="Đăng ký")
async def login(data: LoginRequest, ):
    pass
