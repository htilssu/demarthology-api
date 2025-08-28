from models.user import User
from repositories.repository import PaginatedRepository


class UserRepository(PaginatedRepository[User]):
    pass
