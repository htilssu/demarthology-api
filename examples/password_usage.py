"""
Example usage of the password utility.

This script demonstrates how to use the password hashing and verification
functions for user registration and login scenarios.
"""

from app.utils.password import hash_password, verify_password


def example_user_registration():
    """Example of how to hash a password during user registration."""
    print("=== User Registration Example ===")
    
    # User provides a plain text password during registration
    plain_password = "mySecurePassword123!"
    
    # Hash the password before storing in database
    hashed_password = hash_password(plain_password)
    
    print(f"Original password: {plain_password}")
    print(f"Hashed password (to store in DB): {hashed_password}")
    print(f"Hash length: {len(hashed_password)} characters")
    print()
    
    return hashed_password


def example_user_login(stored_hash: str):
    """Example of how to verify a password during user login."""
    print("=== User Login Example ===")
    
    # User provides password during login
    login_password = "mySecurePassword123!"
    
    # Verify the password against the stored hash
    is_valid = verify_password(login_password, stored_hash)
    
    print(f"Login password: {login_password}")
    print(f"Password is valid: {is_valid}")
    print()
    
    # Test with wrong password
    wrong_password = "wrongPassword"
    is_invalid = verify_password(wrong_password, stored_hash)
    
    print(f"Wrong password: {wrong_password}")
    print(f"Password is valid: {is_invalid}")
    print()


def example_password_security():
    """Example showing password security features."""
    print("=== Password Security Features ===")
    
    password = "samePassword"
    
    # Hash the same password multiple times
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    hash3 = hash_password(password)
    
    print(f"Same password hashed 3 times:")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"Hash 3: {hash3}")
    print()
    
    print("Notice how each hash is different due to random salt!")
    print("But all verify correctly:")
    print(f"Hash 1 verifies: {verify_password(password, hash1)}")
    print(f"Hash 2 verifies: {verify_password(password, hash2)}")
    print(f"Hash 3 verifies: {verify_password(password, hash3)}")
    print()


if __name__ == "__main__":
    print("Password Utility Usage Examples")
    print("=" * 40)
    print()
    
    # Demonstrate registration
    stored_hash = example_user_registration()
    
    # Demonstrate login
    example_user_login(stored_hash)
    
    # Demonstrate security features
    example_password_security()