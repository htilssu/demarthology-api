import json
from fastapi import Depends, HTTPException, status, UploadFile
from typing import List, Optional
from beanie.operators import In
from bson import ObjectId

from app.repositories.question_repository import QuestionRepository
from app.repositories.symptom_repository import SymptomRepository
from app.schemas.question import QuestionCreate
from app.use_cases.usecase import UseCase
from app.utils.upload_img import cloudinary_service


class CreateQuestionUC(UseCase):
    def __init__(
        self,
        question_repo: QuestionRepository = Depends(QuestionRepository),
        symptom_repo: SymptomRepository = Depends(SymptomRepository)
    ):
        self._question_repo = question_repo
        self._symptom_repo = symptom_repo

    async def action(self, *args, **kwargs):
        data: QuestionCreate = args[0]
        author_id: str = args[1]
        files: Optional[List[UploadFile]] = kwargs.get("files", [])

        # --- Parse symptom_ids in case it's passed as a JSON string ---
        symptom_ids = data.symptom_ids
        if (
            isinstance(symptom_ids, list) 
            and len(symptom_ids) == 1 
            and isinstance(symptom_ids[0], str)
        ):
            try:
                parsed = json.loads(symptom_ids[0])
                if isinstance(parsed, list):
                    symptom_ids = parsed
            except json.JSONDecodeError:
                pass  # giữ nguyên nếu không parse được


        # Validate symptoms exist
        if symptom_ids:
            from app.models.symptom import Symptom
            from beanie import PydanticObjectId
            
            
            
            # Convert string IDs to ObjectId
            try:
                object_ids = [PydanticObjectId(id_str) for id_str in symptom_ids]
                
            except Exception as e:
                print(f"ERROR: Failed to convert IDs: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid symptom ID format: {str(e)}"
                )
            
            symptoms = await Symptom.find(
                In(Symptom.id, object_ids)
            ).to_list()
            
            
            
                    
            if len(symptoms) != len(symptom_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Some symptom IDs are invalid. Found {len(symptoms)} of {len(symptom_ids)} symptoms."
                )

        # --- Upload images if provided ---
        image_urls = []
        if files:
            try:
                upload_results = await cloudinary_service.upload_multiple_images(
                    files, folder="questions"
                )
                image_urls = [result["url"] for result in upload_results]
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Image upload failed: {str(e)}"
                )

        # --- Create question ---
        question_data = {
            "title": data.title,
            "content": data.content,
            "symptom_ids": symptom_ids,
            "author_id": author_id,
            "image_urls": image_urls
        }

        question = await self._question_repo.create_question(question_data)

        # --- Get question with symptoms for response ---
        result = await self._question_repo.get_with_symptoms(str(question.id))

        return {
            "success": True,
            "message": "Question created successfully. Waiting for approval.",
            "data": {
                "question": result["question"]
            }
        }

class ListQuestionsUC(UseCase):
    def __init__(self, question_repo: QuestionRepository = Depends(QuestionRepository)):
        self._question_repo = question_repo

    async def action(self, *args, **kwargs):
        skip = kwargs.get("skip", 0)
        limit = kwargs.get("limit", 20)

        # Chỉ lấy questions đã được duyệt
        questions = await self._question_repo.find_approved_questions(skip, limit)

        # Get symptoms for each question
        result = []
        for question in questions:
            symptoms = []
            if question.symptom_ids:
                from app.models.symptom import Symptom
                from beanie import PydanticObjectId
                try:
                    object_ids = [PydanticObjectId(id_str) for id_str in question.symptom_ids]
                    symptoms = await Symptom.find(
                        In(Symptom.id, object_ids)
                    ).to_list()
                except Exception:
                    symptoms = []

            # Truncate content for list view
            content_preview = question.content[:200] + "..." if len(question.content) > 200 else question.content

            result.append({
                "id": str(question.id),
                "title": question.title,
                "content": content_preview,
                "author_id": question.author_id,
                "image_urls": question.image_urls,
                "view_count": question.view_count,
                "upvotes": question.upvotes,
                "downvotes": question.downvotes,
                "is_resolved": question.is_resolved,
                "symptoms": symptoms,
                "answer_count": 0,  # TODO: Count answers when implemented
                "created_at": question.created_at
            })

        return {
            "success": True,
            "data": result,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "count": len(result)
            }
        }


class ListPendingQuestionsUC(UseCase):
    def __init__(self, question_repo: QuestionRepository = Depends(QuestionRepository)):
        self._question_repo = question_repo

    async def action(self, *args, **kwargs):
        skip = kwargs.get("skip", 0)
        limit = kwargs.get("limit", 20)

        # Lấy questions chờ duyệt
        questions = await self._question_repo.find_pending_questions(skip, limit)

        # Get symptoms for each question
        result = []
        for question in questions:
            symptoms = []
            if question.symptom_ids:
                from app.models.symptom import Symptom
                from beanie import PydanticObjectId
                try:
                    object_ids = [PydanticObjectId(id_str) for id_str in question.symptom_ids]
                    symptoms = await Symptom.find(
                        In(Symptom.id, object_ids)
                    ).to_list()
                except Exception:
                    symptoms = []

            # Truncate content for list view
            content_preview = question.content[:200] + "..." if len(question.content) > 200 else question.content

            result.append({
                "id": str(question.id),
                "title": question.title,
                "content": content_preview,
                "author_id": question.author_id,
                "image_urls": question.image_urls,
                "status": question.status,
                "view_count": question.view_count,
                "upvotes": question.upvotes,
                "downvotes": question.downvotes,
                "is_resolved": question.is_resolved,
                "symptoms": symptoms,
                "answer_count": 0, # TODO: Count answers when implemented
                "created_at": question.created_at
            })

        return {
            "success": True,
            "data": result,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "count": len(result)
            }
        }


class GetQuestionDetailUC(UseCase):
    def __init__(self, question_repo: QuestionRepository = Depends(QuestionRepository)):
        self._question_repo = question_repo

    async def action(self, *args, **kwargs):
        question_id: str = args[0]
        
        result = await self._question_repo.get_with_symptoms(question_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )

        # Increment view count
        question = result["question"]
        question.view_count += 1
        await question.save()

        return {
            "success": True,
            "data": {
                "question": question,
                "symptoms": result["symptoms"]
            }
        }
