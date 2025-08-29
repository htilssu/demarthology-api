"""
JWT token utility module for generating and verifying JWT tokens.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import jwt

from app.configs.setting import setting


def generate_token(user_data: Dict[str, Any]) -> str:
    """
    Generate a JWT token for the given user data.
    
    Args:
        user_data (Dict[str, Any]): User data to encode in the token
        
    Returns:
        str: The generated JWT token
    """
    expiration = datetime.utcnow() + timedelta(hours=setting.JWT_EXPIRATION_HOURS)
    
    payload = {
        "user_data": user_data,
        "exp": expiration,
        "iat": datetime.utcnow()
    }
    
    return jwt.encode(payload, setting.JWT_SECRET, algorithm=setting.JWT_ALGORITHM)


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token and return the user data if valid.
    
    Args:
        token (str): The JWT token to verify
        
    Returns:
        Optional[Dict[str, Any]]: User data if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(token, setting.JWT_SECRET, algorithms=[setting.JWT_ALGORITHM])
        return payload.get("user_data")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def extract_token_from_header(authorization_header: str) -> Optional[str]:
    """
    Extract JWT token from Authorization header.
    
    Args:
        authorization_header (str): The Authorization header value
        
    Returns:
        Optional[str]: The extracted token if valid format, None otherwise
    """
    if not authorization_header:
        return None
        
    parts = authorization_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
        
    return parts[1]