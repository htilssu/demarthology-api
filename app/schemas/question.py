from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.question import QuestionStatus


class QuestionCreate(BaseModel):
    title: str = Field(..., min_length=10, max_length=200, description="Tiêu đề câu hỏi")
    content: str = Field(..., min_length=20, description="Nội dung chi tiết câu hỏi")
    symptom_ids: List[str] = Field(default=[], description="Danh sách ID triệu chứng")


class QuestionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=10, max_length=200)
    content: Optional[str] = Field(None, min_length=20)
    symptom_ids: Optional[List[str]] = None


class SymptomResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    image_urls: List[str] = []
    status: QuestionStatus
    view_count: int
    upvotes: int
    downvotes: int
    is_resolved: bool
    created_at: datetime
    symptoms: List[SymptomResponse] = []

    class Config:
        from_attributes = True


class QuestionListItem(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    status: QuestionStatus
    view_count: int
    upvotes: int
    downvotes: int
    is_resolved: bool
    created_at: datetime
    symptoms: List[SymptomResponse] = []
    answer_count: int = 0

    class Config:
        from_attributes = True
