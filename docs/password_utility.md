# Password Utility Documentation

This document explains how to use the password utility functions for secure password handling in the Demarthology API.

## Overview

The password utility provides two main functions:
- `hash_password(password: str) -> str`: Hash a plain text password
- `verify_password(plain_password: str, hashed_password: str) -> bool`: Verify a password

## Features

- Uses bcrypt for secure password hashing
- Automatically generates random salt for each password
- Industry-standard security practices
- Simple and easy-to-use API

## Installation

The password utility requires the `passlib[bcrypt]` package, which is included in the requirements.txt:

```
passlib[bcrypt]
```

## Usage

### Import the functions

```python
from app.utils.password import hash_password, verify_password
```

### User Registration

When a user registers, hash their password before storing it in the database:

```python
from app.utils.password import hash_password

# User provides plain text password
plain_password = "user_password123"

# Hash the password
hashed_password = hash_password(plain_password)

# Store hashed_password in the database (NOT the plain password)
user = User(
    email="user@example.com",
    password=hashed_password,  # Store the hashed version
    first_name="John",
    last_name="Doe",
    dob=datetime.now()
)
```

### User Login

When a user logs in, verify their password against the stored hash:

```python
from app.utils.password import verify_password

# Get user from database
user = await user_repository.find_by_email(email)

# Verify the provided password against the stored hash
if user and verify_password(provided_password, user.password):
    # Login successful
    return {"success": True, "message": "Login successful"}
else:
    # Login failed
    return {"success": False, "message": "Invalid credentials"}
```

## Security Features

1. **Salt**: Each password hash includes a unique random salt
2. **Cost Factor**: Uses bcrypt with appropriate cost factor for security
3. **No Plain Text**: Plain text passwords are never stored
4. **Timing Attack Resistant**: Verification time is consistent

## Example Integration

See the `examples/password_usage.py` file for complete usage examples.

## Testing

Run the password utility tests:

```bash
python -m unittest tests.test_password_utils -v
```

## Important Notes

1. **Never store plain text passwords** - always hash them first
2. **Always use verify_password()** for login verification
3. **Each hash is unique** - the same password will produce different hashes due to salt
4. **Hashes are one-way** - you cannot convert a hash back to the original password