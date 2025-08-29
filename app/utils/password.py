"""
Password utility module for hashing and verifying passwords using bcrypt.
"""

from passlib.context import CryptContext

# Create a password context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordUtils:
    """Utility class for password operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain text password using bcrypt.

        Args:
            password (str): The plain text password to hash

        Returns:
            str: The hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain text password against a hashed password.

        Args:
            plain_password (str): The plain text password to verify
            hashed_password (str): The hashed password to verify against

        Returns:
            bool: True if the password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)


# Keep backward compatibility with existing function-based usage
def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password (str): The plain text password to hash

    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The hashed password to verify against

    Returns:
        bool: True if the password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
