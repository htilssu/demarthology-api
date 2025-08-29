# CurrentUserService và JWT Authentication

Tài liệu này mô tả việc triển khai CurrentUserService và hệ thống xác thực JWT cho demarthology-api.

## Tổng quan

Hệ thống xác thực bao gồm:

1. **CurrentUserService** - Service để xác thực và lấy thông tin người dùng từ JWT token
2. **JWT Token Utilities** - Các hàm utility để tạo và xác thực JWT token
3. **UnauthorizedException** - Exception tùy chỉnh cho các lỗi xác thực
4. **Cập nhật LoginUC** - Tạo JWT token khi đăng nhập thành công

## Các thành phần chính

### 1. CurrentUserService

**File:** `app/services/current_user_service.py`

```python
from app.services.current_user_service import CurrentUserService

service = CurrentUserService()

# Lấy thông tin user từ Request (Authorization header)
user_data = service.get_current_user(request)

# Lấy thông tin user từ token string
user_data = service.get_current_user_from_token(token)
```

**Phương thức:**
- `get_current_user(request: Request)` - Lấy thông tin user từ Authorization header
- `get_current_user_from_token(token: str)` - Lấy thông tin user từ JWT token

### 2. JWT Token Utilities

**File:** `app/utils/jwt_token.py`

```python
from app.utils.jwt_token import generate_token, verify_token, extract_token_from_header

# Tạo token
user_data = {"email": "user@example.com", "first_name": "John", "last_name": "Doe"}
token = generate_token(user_data)

# Xác thực token
user_data = verify_token(token)  # Returns user_data or None

# Trích xuất token từ header
token = extract_token_from_header("Bearer abc123xyz")  # Returns "abc123xyz"
```

### 3. UnauthorizedException

**File:** `app/errors/unauthorized.py`

```python
from app.errors.unauthorized import UnauthorizedException

# Ném exception với message mặc định
raise UnauthorizedException()

# Ném exception với message tùy chỉnh
raise UnauthorizedException("Token expired")

# Ném exception với message và detail
raise UnauthorizedException("Invalid token", "Please login again")
```

### 4. Cấu hình JWT

**File:** `app/configs/setting.py`

Các setting JWT đã được thêm:
- `JWT_SECRET` - Key bí mật để ký token (đổi trong production)
- `JWT_ALGORITHM` - Thuật toán mã hóa (mặc định: HS256)
- `JWT_EXPIRATION_HOURS` - Thời gian hết hạn token (mặc định: 24 giờ)

## Cách sử dụng

### 1. Đăng nhập và nhận token

```python
# POST /login
{
    "email": "user@example.com",
    "password": "yourpassword"
}

# Response:
{
    "success": true,
    "message": "Login successful",
    "user": {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

### 2. Sử dụng token để truy cập protected endpoints

```python
# Thêm Authorization header trong request:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 3. Tạo protected route

```python
from fastapi import APIRouter, Request, HTTPException, status
from app.services.current_user_service import CurrentUserService
from app.errors.unauthorized import UnauthorizedException

router = APIRouter()
current_user_service = CurrentUserService()

@router.get("/profile")
async def get_profile(request: Request):
    try:
        user_data = current_user_service.get_current_user(request)
        return {"user": user_data}
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
```

### 4. Sử dụng với FastAPI Dependencies

```python
from fastapi import Depends
from app.services.current_user_service import CurrentUserService
from app.errors.unauthorized import UnauthorizedException

def get_current_user_service() -> CurrentUserService:
    return CurrentUserService()

def get_current_user(
    request: Request, 
    user_service: CurrentUserService = Depends(get_current_user_service)
):
    try:
        return user_service.get_current_user(request)
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/protected")
async def protected_endpoint(current_user = Depends(get_current_user)):
    return {"message": f"Hello {current_user['first_name']}!"}
```

## Xử lý lỗi

### Các trường hợp ném UnauthorizedException:

1. **Không có Authorization header**
   - Message: "Authorization header is required"

2. **Format Authorization header không đúng**
   - Message: "Invalid Authorization header format. Expected: Bearer <token>"

3. **Token không hợp lệ hoặc hết hạn**
   - Message: "Invalid or expired token"

### Chuyển đổi thành HTTPException:

```python
try:
    user_data = current_user_service.get_current_user(request)
except UnauthorizedException as e:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=e.message,
        headers={"WWW-Authenticate": "Bearer"},
    )
```

## Testing

Các test cases đã được tạo cho:

1. **JWT Token Utilities** (`tests/test_jwt_token.py`)
2. **UnauthorizedException** (`tests/test_unauthorized.py`)
3. **CurrentUserService** (`tests/test_current_user_service.py`)
4. **Login Integration** (`tests/test_login_jwt_integration.py`)

Chạy tests:

```bash
# Chạy tất cả tests liên quan
python -m unittest tests.test_jwt_token tests.test_unauthorized tests.test_current_user_service tests.test_login_jwt_integration -v

# Chạy từng test riêng
python -m unittest tests.test_current_user_service -v
```

## Bảo mật

### Lưu ý quan trọng:

1. **Đổi JWT_SECRET trong production** - Sử dụng key bí mật mạnh và bảo mật
2. **Sử dụng HTTPS** - Luôn truyền token qua HTTPS trong production
3. **Thời gian hết hạn** - Cân nhắc thời gian hết hạn phù hợp (mặc định 24h)
4. **Refresh token** - Có thể thêm refresh token mechanism trong tương lai
5. **Token blacklist** - Có thể thêm blacklist để vô hiệu hóa token khi cần

### Environment Variables:

Thêm vào file `.env`:

```env
JWT_SECRET=your-very-secure-secret-key-for-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

## Examples

Xem các file example:
- `examples/current_user_service_usage.py` - Cách sử dụng CurrentUserService
- `examples/protected_routes_example.py` - Ví dụ protected routes hoàn chỉnh