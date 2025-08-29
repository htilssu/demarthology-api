from typing import List, Optional

from app.models.question import Question, QuestionStatus
from app.models.symptom import Symptom
from app.repositories.repository import PaginatedRepository


class QuestionRepository(PaginatedRepository[Question]):
    document_class = Question

    async def create_question(self, question_data: dict) -> Question:
        """Create new question with PENDING status"""
        question = Question(**question_data)
        question.status = QuestionStatus.PENDING
        return await question.insert()

    async def find_approved_questions(self, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get only approved questions"""
        return await Question.find(Question.status == QuestionStatus.APPROVED).skip(skip).limit(limit).to_list()

    async def find_all_questions(self, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get all questions regardless of status (for testing/admin)"""
        return await Question.find().skip(skip).limit(limit).to_list()

    async def find_pending_questions(self, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get only pending questions (for admin approval)"""
        return (
            await Question.find(Question.status == QuestionStatus.PENDING)
            .skip(skip)
            .limit(limit)
            .sort([("created_at", -1)])
            .to_list()
        )

    async def find_by_author(self, author_id: str) -> List[Question]:
        """Get questions by author (including pending)"""
        return await Question.find(Question.author_id == author_id).sort([("created_at", -1)]).to_list()

    async def find_by_symptom_ids(self, symptom_ids: List[str]) -> List[Question]:
        """Find approved questions by symptom IDs"""
        from beanie import PydanticObjectId
        from beanie.operators import In

        try:
            object_ids = [PydanticObjectId(id_str) for id_str in symptom_ids]
            return await Question.find(
                In(Question.symptom_ids, object_ids), Question.status == QuestionStatus.APPROVED
            ).to_list()
        except Exception as e:
            print(f"Error finding questions by symptom IDs: {e}")
            return []

    async def add_images_to_question(self, question_id: str, image_urls: List[str]) -> Question:
        """Add image URLs to existing question"""
        question = await Question.get(question_id)
        question.image_urls.extend(image_urls)
        return await question.save()

    async def get_with_symptoms(self, question_id: str) -> Optional[dict]:
        """Get question with populated symptoms"""
        question = await Question.get(question_id)
        if not question:
            return None

        symptoms = []
        if question.symptom_ids:
            from beanie import PydanticObjectId
            from beanie.operators import In

            # Convert string IDs to ObjectId
            try:
                object_ids = [PydanticObjectId(id_str) for id_str in question.symptom_ids]
                symptoms = await Symptom.find(In(Symptom.id, object_ids)).to_list()
            except Exception as e:
                print(f"Error finding symptoms: {e}")
                symptoms = []

        return {"question": question, "symptoms": symptoms}
