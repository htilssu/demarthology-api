from fastapi import APIRouter, Depends, Request

from app.schemas.forgot_password_request import ForgotPasswordRequest
from app.schemas.login_request import LoginRequest
from app.schemas.login_response import LoginResponse
from app.schemas.register_request import RegisterRequest
from app.schemas.register_response import RegisterResponse
from app.schemas.reset_password_request import ResetPasswordRequest
from app.use_cases.forgot_password_uc import ForgotPasswordUC
from app.use_cases.login_uc import LoginUC
from app.use_cases.logout_uc import LogoutUC
from app.use_cases.register_uc import RegisterUC
from app.use_cases.reset_password_uc import ResetPasswordUC
from app.use_cases.usecase import UseCase

router = APIRouter(tags=["Authentication"])


@router.post("/login", summary="Đăng nhập", response_model=LoginResponse)
async def login(data: LoginRequest, uc: UseCase = Depends(LoginUC)):
    return await uc.action(data)


@router.post("/register", summary="Đăng ký", response_model=RegisterResponse)
async def register(data: RegisterRequest, uc: UseCase = Depends(RegisterUC)):
    return await uc.action(data)


@router.post("/forgot-password", summary="Quên mật khẩu")
async def forgot_password(data: ForgotPasswordRequest, uc: UseCase = Depends(ForgotPasswordUC)):
    return await uc.action(data)


@router.post("/reset-password", summary="Đặt lại mật khẩu")
async def reset_password(data: ResetPasswordRequest, uc: UseCase = Depends(ResetPasswordUC)):
    return await uc.action(data)


@router.post("/logout", summary="Đăng xuất")
async def logout(request: Request, uc: UseCase = Depends(LogoutUC)):
    return await uc.action(request)
