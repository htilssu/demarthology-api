from typing import Optional, List
from enum import Enum

from app.models.base import Base


class AnswerStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved" 
    REJECTED = "rejected"


class Answer(Base):
    content: str
    question_id: str  # Reference to Question._id
    author_id: str    # Reference to User._id
    
    # Images từ Cloudinary (nếu cần)
    image_urls: List[str] = []
    

    # Engagement
    upvotes: int = 0
    downvotes: int = 0
    is_accepted: bool = False
    
    # Nested replies
    parent_answer_id: Optional[str] = None  # For threaded comments
    
    class Settings:
        name = "answers"
