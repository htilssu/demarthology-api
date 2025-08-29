from fastapi import APIRouter, Depends, File, UploadFile, Form, Query
from typing import List, Optional
import json

from app.schemas.question import QuestionCreate
from app.use_cases.question_uc import (
    CreateQuestionUC,
    ListQuestionsUC,
    ListPendingQuestionsUC,
    GetQuestionDetailUC
)
from app.use_cases.usecase import UseCase

router = APIRouter(tags=["Questions"])


@router.post("", summary="Tạo câu hỏi mới")
async def create_question(
    title: str = Form(..., min_length=10, max_length=200, description="Tiêu đề câu hỏi"),
    content: str = Form(..., min_length=20, description="Nội dung chi tiết câu hỏi"),
    symptom_ids: Optional[str] = Form(None, description="Danh sách ID triệu chứng (cách nhau bởi dấu phẩy). VD: id1,id2,id3"),
    # author_id: str = Form(..., description="ID người tạo câu hỏi"),  # Tạm thời tắt
    files: List[UploadFile] = File(default=[], description="Chọn nhiều hình ảnh minh họa (tùy chọn)"),
    uc: UseCase = Depends(CreateQuestionUC)
):
    """
    ## Tạo câu hỏi mới với multipart/form-data
    
    ### Các trường bắt buộc:
    - **title**: Tiêu đề câu hỏi (10-200 ký tự)
    - **content**: Nội dung chi tiết (tối thiểu 20 ký tự)
    
    ### Các trường tùy chọn:
    - **symptom_ids**: Danh sách ID triệu chứng, cách nhau bởi dấu phẩy
    - **files**: Upload nhiều hình ảnh minh họa
    
    ### Quy trình:
    1. Câu hỏi được tạo với trạng thái PENDING
    2. Admin sẽ duyệt và chuyển thành APPROVED
    3. Chỉ câu hỏi APPROVED mới hiển thị công khai
    """
    # Parse symptom_ids từ string (hỗ trợ cả JSON array và comma-separated)
    parsed_symptom_ids = []
    if symptom_ids:
        try:
            # Thử parse như JSON array trước: ["id1", "id2"]
            parsed_symptom_ids = json.loads(symptom_ids)
            if not isinstance(parsed_symptom_ids, list):
                raise ValueError("Not a list")
        except (json.JSONDecodeError, ValueError):
            # Nếu không phải JSON, parse như comma-separated: id1,id2
            parsed_symptom_ids = [id.strip() for id in symptom_ids.split(",") if id.strip()]

    question_data = QuestionCreate(
        title=title,
        content=content,
        symptom_ids=parsed_symptom_ids
    )

    # Sử dụng author_id mặc định tạm thời
    default_author_id = "default_user_123"
    
    return await uc.action(question_data, default_author_id, files=files)


@router.get("", summary="Danh sách câu hỏi đã duyệt")
async def list_questions(
    skip: int = Query(0, ge=0, description="Số câu hỏi bỏ qua"),
    limit: int = Query(20, ge=1, le=100, description="Số câu hỏi tối đa"),
    uc: UseCase = Depends(ListQuestionsUC)
):
    """Lấy danh sách câu hỏi đã được duyệt (status = approved)"""
    return await uc.action(skip=skip, limit=limit)


@router.get("/pending", summary="Danh sách câu hỏi chờ duyệt")
async def list_pending_questions(
    skip: int = Query(0, ge=0, description="Số câu hỏi bỏ qua"),
    limit: int = Query(20, ge=1, le=100, description="Số câu hỏi tối đa"),
    uc: UseCase = Depends(ListPendingQuestionsUC)
):
    """
    Lấy danh sách câu hỏi chờ duyệt (status = pending)
    
    Endpoint này dành cho admin để review và approve/reject questions
    """
    return await uc.action(skip=skip, limit=limit)


@router.get("/{question_id}", summary="Chi tiết câu hỏi")
async def get_question_detail(
    question_id: str,
    uc: UseCase = Depends(GetQuestionDetailUC)
):
    """Lấy chi tiết câu hỏi kèm theo symptoms"""
    return await uc.action(question_id)
