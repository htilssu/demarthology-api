from enum import Enum

from app.models.base import Base


class VoteType(str, Enum):
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"


class TargetType(str, Enum):
    QUESTION = "question"
    ANSWER = "answer"


class Vote(Base):
    user_id: str
    target_id: str  # ID của Question hoặc Answer
    target_type: TargetType
    vote_type: VoteType

    class Settings:
        name = "votes"

    class Config:
        # Ensure unique vote per user per target
        indexes = [
            [("user_id", 1), ("target_id", 1), ("target_type", 1)],
            {"unique": True},
            [("target_id", 1), ("target_type", 1)],  # để đếm vote nhanh
        ]
