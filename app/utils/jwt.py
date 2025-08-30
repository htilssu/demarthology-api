from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from fastapi import HTTPException, status


class JWTUtils:
    """JWT utility class for token creation and validation."""

    SECRET_KEY = "your-secret-key-change-in-production"  # Should be in settings
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    RESET_TOKEN_EXPIRE_MINUTES = 15  # Reset tokens expire faster

    @classmethod
    def create_access_token(cls, data: Dict[str, Any]) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_access_token(cls, token: str) -> Dict[str, Any]:
        """Decode and validate a JWT access token."""
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    @classmethod
    def create_reset_token(cls, email: str) -> str:
        """Create a password reset token."""
        data = {"email": email, "type": "reset"}
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=cls.RESET_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_reset_token(cls, token: str) -> str:
        """Decode and validate a password reset token. Returns email."""
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            if payload.get("type") != "reset":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type")
            return payload.get("email")
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset token")

    @classmethod
    def verify_reset_token(cls, token: str) -> Dict[str, Any] | None:
        """Verify a password reset token and return payload if valid."""
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            if payload.get("type") != "reset":
                return None
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
