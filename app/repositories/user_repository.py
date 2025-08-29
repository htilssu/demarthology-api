from app.models.user import User
from app.repositories.repository import PaginatedRepository


class UserRepository(PaginatedRepository[User]):
    pass
