"""
Integration tests for register use case with permission system.
"""

import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException

from app.models.user import User
from app.schemas.register_request import RegisterRequest
from app.services.user_service import UserService
from app.use_cases.register_uc import RegisterUC
from app.utils.authorize import (
    BasicContext,
    UserPermission,
    AdminPermission,
    SelfOrAdminPermission,
    authorize,
)


class TestRegisterPermissionIntegration(unittest.IsolatedAsyncioTestCase):
    """Test cases for register use case integration with permission system."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_user_service = AsyncMock(spec=UserService)
        self.register_uc = RegisterUC(user_service=self.mock_user_service)

    async def test_new_user_has_user_permission(self):
        """Test that newly registered users have user permission."""
        # Arrange
        register_request = RegisterRequest(
            email="newuser@example.com",
            password="Password123!",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user doesn't exist
        self.mock_user_service.check_user_exist.return_value = False

        # Mock the User creation and save_user method
        mock_user = MagicMock(spec=User)
        mock_user.email = "newuser@example.com"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"
        mock_user.id = "user123"
        self.mock_user_service.save_user.return_value = mock_user

        with unittest.mock.patch("app.use_cases.register_uc.User", return_value=mock_user):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert registration was successful
            self.assertTrue(result.success)
            
            # Test that the new user has UserPermission
            context = BasicContext(user=mock_user)
            permission = UserPermission()
            has_permission = await permission.authorize(context)
            self.assertTrue(has_permission)

    async def test_new_user_cannot_access_admin_features(self):
        """Test that newly registered users cannot access admin features."""
        # Arrange
        register_request = RegisterRequest(
            email="newuser@example.com",
            password="Password123!",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user doesn't exist
        self.mock_user_service.check_user_exist.return_value = False

        # Mock the User creation and save_user method
        mock_user = MagicMock(spec=User)
        mock_user.email = "newuser@example.com"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"
        mock_user.id = "user123"
        self.mock_user_service.save_user.return_value = mock_user

        with unittest.mock.patch("app.use_cases.register_uc.User", return_value=mock_user):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert registration was successful
            self.assertTrue(result.success)
            
            # Test that the new user CANNOT access admin features
            context = BasicContext(user=mock_user)
            admin_permission = AdminPermission()
            has_admin_permission = await admin_permission.authorize(context)
            self.assertFalse(has_admin_permission)

    async def test_new_user_can_access_own_data(self):
        """Test that newly registered users can access their own data."""
        # Arrange
        register_request = RegisterRequest(
            email="newuser@example.com",
            password="Password123!",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user doesn't exist
        self.mock_user_service.check_user_exist.return_value = False

        # Mock the User creation and save_user method
        mock_user = MagicMock(spec=User)
        mock_user.email = "newuser@example.com"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"
        mock_user.id = "user123"
        self.mock_user_service.save_user.return_value = mock_user

        with unittest.mock.patch("app.use_cases.register_uc.User", return_value=mock_user):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert registration was successful
            self.assertTrue(result.success)
            
            # Test that the new user can access their own data
            from app.utils.authorize import ResourceOwnerContext
            
            # Create a resource owned by the user
            user_resource = MagicMock()
            user_resource.user_id = "user123"
            
            context = ResourceOwnerContext(user=mock_user, obj=user_resource)
            self_or_admin_permission = SelfOrAdminPermission()
            can_access_own_data = await self_or_admin_permission.authorize(context)
            self.assertTrue(can_access_own_data)

    async def test_new_user_cannot_access_others_data(self):
        """Test that newly registered users cannot access other users' data."""
        # Arrange
        register_request = RegisterRequest(
            email="newuser@example.com",
            password="Password123!",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user doesn't exist
        self.mock_user_service.check_user_exist.return_value = False

        # Mock the User creation and save_user method
        mock_user = MagicMock(spec=User)
        mock_user.email = "newuser@example.com"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"
        mock_user.id = "user123"
        self.mock_user_service.save_user.return_value = mock_user

        with unittest.mock.patch("app.use_cases.register_uc.User", return_value=mock_user):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert registration was successful
            self.assertTrue(result.success)
            
            # Test that the new user CANNOT access other users' data
            from app.utils.authorize import ResourceOwnerContext
            
            # Create a resource owned by another user
            other_user_resource = MagicMock()
            other_user_resource.user_id = "other_user456"
            
            context = ResourceOwnerContext(user=mock_user, obj=other_user_resource)
            self_or_admin_permission = SelfOrAdminPermission()
            can_access_others_data = await self_or_admin_permission.authorize(context)
            self.assertFalse(can_access_others_data)

    async def test_authorize_function_with_new_user(self):
        """Test the authorize utility function with a newly registered user."""
        # Arrange
        register_request = RegisterRequest(
            email="newuser@example.com",
            password="Password123!",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user doesn't exist
        self.mock_user_service.check_user_exist.return_value = False

        # Mock the User creation and save_user method
        mock_user = MagicMock(spec=User)
        mock_user.email = "newuser@example.com"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"
        mock_user.id = "user123"
        self.mock_user_service.save_user.return_value = mock_user

        with unittest.mock.patch("app.use_cases.register_uc.User", return_value=mock_user):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert registration was successful
            self.assertTrue(result.success)
            
            # Test authorize function allows user permission
            context = BasicContext(user=mock_user)
            permission = UserPermission()
            
            # Should not raise exception
            await authorize(permission, context)

    async def test_authorize_function_denies_admin_access_for_new_user(self):
        """Test the authorize utility function denies admin access for new users."""
        # Arrange
        register_request = RegisterRequest(
            email="newuser@example.com",
            password="Password123!",
            first_name="John",
            last_name="Doe",
            dob=datetime(1990, 1, 1),
        )

        # Mock that user doesn't exist
        self.mock_user_service.check_user_exist.return_value = False

        # Mock the User creation and save_user method
        mock_user = MagicMock(spec=User)
        mock_user.email = "newuser@example.com"
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role = "user"
        mock_user.id = "user123"
        self.mock_user_service.save_user.return_value = mock_user

        with unittest.mock.patch("app.use_cases.register_uc.User", return_value=mock_user):
            # Act
            result = await self.register_uc.action(register_request)

            # Assert registration was successful
            self.assertTrue(result.success)
            
            # Test authorize function denies admin permission
            context = BasicContext(user=mock_user)
            admin_permission = AdminPermission()
            
            # Should raise HTTPException
            with self.assertRaises(HTTPException) as exc_context:
                await authorize(admin_permission, context)
            
            self.assertEqual(exc_context.exception.status_code, 403)
            self.assertEqual(exc_context.exception.detail, "Insufficient permissions")


class TestPermissionContextsForRegistration(unittest.IsolatedAsyncioTestCase):
    """Test cases for permission contexts used in registration scenarios."""

    def test_basic_context_with_new_user(self):
        """Test BasicContext with newly registered user data."""
        # Arrange
        mock_user = MagicMock(spec=User)
        mock_user.email = "newuser@example.com"
        mock_user.role = "user"
        mock_user.id = "user123"

        # Act
        context = BasicContext(user=mock_user)

        # Assert
        self.assertEqual(context.get_user(), mock_user)
        self.assertIsNone(context.get_obj())

    def test_resource_owner_context_with_new_user(self):
        """Test ResourceOwnerContext with newly registered user data."""
        # Arrange
        mock_user = MagicMock(spec=User)
        mock_user.email = "newuser@example.com"
        mock_user.role = "user"
        mock_user.id = "user123"

        mock_resource = MagicMock()
        mock_resource.user_id = "user123"

        # Act
        from app.utils.authorize import ResourceOwnerContext
        context = ResourceOwnerContext(user=mock_user, obj=mock_resource)

        # Assert
        self.assertEqual(context.get_user(), mock_user)
        self.assertEqual(context.get_obj(), mock_resource)


if __name__ == "__main__":
    unittest.main()