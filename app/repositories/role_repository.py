from typing import Optional

from app.models.role import Role
from app.repositories.repository import Repository


class RoleRepository(Repository[Role]):
    def __init__(self):
        super().__init__(Role)

    async def find_by_name(self, name: str) -> Optional[Role]:
        """Find a role by name."""
        return await self.model.find_one(Role.name == name)

    async def find_active_roles(self) -> list[Role]:
        """Find all active roles."""
        return await self.model.find(Role.is_active == True).to_list()  # noqa: E712
