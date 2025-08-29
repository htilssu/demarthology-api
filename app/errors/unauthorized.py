from typing import Optional


class UnauthorizedException(Exception):
    
    def __init__(self, message: str = "Unauthorized", detail: Optional[str] = None) -> None:
        self.message = message
        self.detail = detail
        super().__init__(message)