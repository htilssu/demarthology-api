from typing import Optional

from fastapi import Depends, HTTPException, status

from app.models.role import Role
from app.repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, role_repository: RoleRepository = Depends(RoleRepository)):
        self._role_repository = role_repository

    async def get_role_by_name(self, name: str) -> Optional[Role]:
        """Get a role by name."""
        try:
            return await self._role_repository.find_by_name(name)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error finding role: {str(e)}",
            )

    async def get_or_create_default_role(self) -> Role:
        """Get or create the default 'user' role."""
        role = await self.get_role_by_name("user")
        if not role:
            # Create default user role if it doesn't exist
            role = await self.create_role("user", "Default user role")
        return role

    async def create_role(self, name: str, description: str = None) -> Role:
        """Create a new role."""
        try:
            role = Role(name=name, description=description)
            return await self._role_repository.create(role)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating role: {str(e)}",
            )

    async def get_active_roles(self) -> list[Role]:
        """Get all active roles."""
        try:
            return await self._role_repository.find_active_roles()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching roles: {str(e)}",
            )
