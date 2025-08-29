from app.models.user import User
from app.repositories.repository import PaginatedRepository


class UserRepository(PaginatedRepository[User]):
    document_class = User
    
    async def find_by_email(self, email: str) -> User | None:
        """Find a user by email address."""
        return await User.find_one(User.email == email)
