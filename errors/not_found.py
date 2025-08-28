from typing import Optional


class NotFoundException(Exception):

    def __init__(self, message: str, search_criteria: Optional[str]) -> None:
        self.message = message
        self.search_criteria = search_criteria
