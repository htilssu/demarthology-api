# Authentication Middleware Documentation

## Overview

This authentication middleware provides JWT-based authentication for the FastAPI application. It automatically validates JWT tokens on protected routes and provides user context to route handlers.

## Features

- JWT token generation and validation
- Password hashing with bcrypt
- Automatic authentication on protected routes
- User registration and login endpoints
- Current user context in route handlers

## Configuration

Add the following environment variables to your `.env` file:

```env
JWT_SECRET_KEY=your-super-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Usage

### Protected Routes

Routes are automatically protected unless they are in the exempt paths list. To access a protected route, include the JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Exempt Routes

The following routes don't require authentication:
- `/` (root)
- `/docs` (API documentation)
- `/openapi.json` (OpenAPI spec)
- `/redoc` (ReDoc documentation)
- `/login` (user login)
- `/register` (user registration)
- `/health` (health check)

### Getting Current User in Route Handlers

Use the `get_current_user` dependency to access the authenticated user:

```python
from app.dependencies.auth import get_current_user
from app.models.user import User

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {"user_id": str(current_user.id), "email": current_user.email}
```

### API Endpoints

#### POST /login
Login with email and password to get a JWT token.

Request:
```json
{
  "username": "user@example.com",
  "password": "password123",
  "remember_me": false
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### POST /register
Register a new user account.

Request:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "dob": "1990-01-01T00:00:00"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### GET /me
Get current user profile (requires authentication).

Response:
```json
{
  "id": "...",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "dob": "1990-01-01T00:00:00"
}
```

## Security Features

- Passwords are hashed using bcrypt
- JWT tokens have configurable expiration
- Protected routes automatically validate tokens
- Invalid tokens result in 401 Unauthorized responses
- User credentials are validated against the database