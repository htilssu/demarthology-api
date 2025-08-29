"""
CurrentUserService for handling user authentication via JWT tokens.
"""

from typing import Optional, Dict, Any
from fastapi import Request, Depends

from app.errors.unauthorized import UnauthorizedException
from app.utils.jwt_token import extract_token_from_header, verify_token
from app.repositories.user_repository import UserRepository
from app.models.user import User


class CurrentUserService:
    """Service for managing current user authentication."""
    
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self._user_repository = user_repository
    
    async def get_current_user(self, request: Request) -> User:
        """
        Get current user object from Authorization header.
        
        Args:
            request (Request): FastAPI request object
            
        Returns:
            User: Complete user object from database
            
        Raises:
            UnauthorizedException: If no valid token is provided or user not found
        """
        # Extract Authorization header
        authorization_header = request.headers.get("Authorization")
        
        if not authorization_header:
            raise UnauthorizedException("Authorization header is required")
        
        # Extract token from header
        token = extract_token_from_header(authorization_header)
        
        if not token:
            raise UnauthorizedException("Invalid Authorization header format. Expected: Bearer <token>")
        
        # Verify token and get user data
        user_data = verify_token(token)
        
        if not user_data:
            raise UnauthorizedException("Invalid or expired token")
        
        # Get user email from token data
        email = user_data.get("email")
        if not email:
            raise UnauthorizedException("Invalid token: missing user email")
        
        # Fetch user from database
        user = await self._user_repository.find_by_email(email)
        if not user:
            raise UnauthorizedException("User not found")
        
        return user
    
    async def get_current_user_from_token(self, token: str) -> User:
        """
        Get current user object from JWT token string.
        
        Args:
            token (str): JWT token string
            
        Returns:
            User: Complete user object from database
            
        Raises:
            UnauthorizedException: If token is invalid or user not found
        """
        user_data = verify_token(token)
        
        if not user_data:
            raise UnauthorizedException("Invalid or expired token")
        
        # Get user email from token data
        email = user_data.get("email")
        if not email:
            raise UnauthorizedException("Invalid token: missing user email")
        
        # Fetch user from database
        user = await self._user_repository.find_by_email(email)
        if not user:
            raise UnauthorizedException("User not found")
        
        return user