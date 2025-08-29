"""
Tests for password utility functions.
"""

import unittest

from app.utils.password import hash_password, verify_password


class TestPasswordUtils(unittest.TestCase):
    """Test cases for password hashing and verification."""

    def test_hash_password(self):
        """Test that hash_password returns a hashed password."""
        password = "testpassword123"
        hashed = hash_password(password)

        # Check that the hashed password is not the same as the original
        self.assertNotEqual(password, hashed)

        # Check that the hashed password is a string
        self.assertIsInstance(hashed, str)

        # Check that the hashed password starts with bcrypt identifier
        self.assertTrue(hashed.startswith("$2b$"))

    def test_verify_password_correct(self):
        """Test that verify_password returns True for correct passwords."""
        password = "testpassword123"
        hashed = hash_password(password)

        # Verify that the correct password returns True
        self.assertTrue(verify_password(password, hashed))

    def test_verify_password_incorrect(self):
        """Test that verify_password returns False for incorrect passwords."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)

        # Verify that an incorrect password returns False
        self.assertFalse(verify_password(wrong_password, hashed))

    def test_different_passwords_produce_different_hashes(self):
        """Test that different passwords produce different hashes."""
        password1 = "password1"
        password2 = "password2"

        hash1 = hash_password(password1)
        hash2 = hash_password(password2)

        # Different passwords should produce different hashes
        self.assertNotEqual(hash1, hash2)

    def test_same_password_produces_different_hashes(self):
        """Test that the same password produces different hashes due to salt."""
        password = "testpassword123"

        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Same password should produce different hashes due to random salt
        self.assertNotEqual(hash1, hash2)

        # But both should verify correctly
        self.assertTrue(verify_password(password, hash1))
        self.assertTrue(verify_password(password, hash2))


if __name__ == "__main__":
    unittest.main()
