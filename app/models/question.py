from datetime import datetime
from enum import Enum
from typing import List, Optional

from app.models.base import Base


class QuestionStatus(str, Enum):
    PENDING = "pending"  # Chờ duyệt
    APPROVED = "approved"  # Đã duyệt
    REJECTED = "rejected"  # Bị từ chối


class Question(Base):
    title: str
    content: str

    # Sử dụng Symptom thay vì Tag
    symptom_ids: List[str] = []  # References to Symptom._id

    # User info
    author_id: str  # Reference to User._id

    # Images từ Cloudinary
    image_urls: List[str] = []  # Cloudinary URLs

    # Moderation
    status: QuestionStatus = QuestionStatus.PENDING
    moderated_by: Optional[str] = None  # Admin/Doctor ID who approved/rejected
    moderated_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None

    # Engagement
    view_count: int = 0
    upvotes: int = 0
    downvotes: int = 0

    # Resolution
    is_resolved: bool = False
    accepted_answer_id: Optional[str] = None

    class Settings:
        name = "questions"
