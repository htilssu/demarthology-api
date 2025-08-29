from fastapi import APIRouter, Depends, Query

from app.schemas.symptom import SymptomCreate, SymptomUpdate
from app.use_cases.symptom_uc import (
    CreateSymptomUC,
    DeleteSymptomUC,
    GetSymptomUC,
    ListSymptomsUC,
    UpdateSymptomUC,
)
from app.use_cases.usecase import UseCase

router = APIRouter(tags=["Symptoms"])


# todo: add auth
@router.post("", summary="Tạo triệu chứng")
async def create_symptom(data: SymptomCreate, uc: UseCase = Depends(CreateSymptomUC)):
    return await uc.action(data)


@router.get("", summary="Danh sách triệu chứng")
async def list_symptoms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    uc: UseCase = Depends(ListSymptomsUC),
):
    return await uc.action(skip=skip, limit=limit)


@router.get("/{id}", summary="Lấy chi tiết triệu chứng")
async def get_symptom(id: str, uc: UseCase = Depends(GetSymptomUC)):
    return await uc.action(id)


# todo: add auth
@router.put("/{id}", summary="Cập nhật triệu chứng")
async def update_symptom(id: str, data: SymptomUpdate, uc: UseCase = Depends(UpdateSymptomUC)):
    return await uc.action(id, data)


# todo: add auth
@router.delete("/{id}", summary="Xóa triệu chứng")
async def delete_symptom(id: str, uc: UseCase = Depends(DeleteSymptomUC)):
    return await uc.action(id)
