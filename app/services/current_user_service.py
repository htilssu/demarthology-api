"""
CurrentUserService for handling user authentication via JWT tokens.
"""

from typing import Optional, Dict, Any
from fastapi import Request

from app.errors.unauthorized import UnauthorizedException
from app.utils.jwt_token import extract_token_from_header, verify_token


class CurrentUserService:
    """Service for managing current user authentication."""
    
    def get_current_user(self, request: Request) -> Dict[str, Any]:
        """
        Get current user information from Authorization header.
        
        Args:
            request (Request): FastAPI request object
            
        Returns:
            Dict[str, Any]: User data from valid JWT token
            
        Raises:
            UnauthorizedException: If no valid token is provided
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
        
        return user_data
    
    def get_current_user_from_token(self, token: str) -> Dict[str, Any]:
        """
        Get current user information from JWT token string.
        
        Args:
            token (str): JWT token string
            
        Returns:
            Dict[str, Any]: User data from valid JWT token
            
        Raises:
            UnauthorizedException: If token is invalid
        """
        user_data = verify_token(token)
        
        if not user_data:
            raise UnauthorizedException("Invalid or expired token")
        
        return user_data