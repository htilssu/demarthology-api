from fastapi import Depends

from app.repositories.symptom_repository import SymptomRepository
from app.schemas.symptom import SymptomCreate, SymptomUpdate
from app.use_cases.usecase import UseCase


class CreateSymptomUC(UseCase):
    def __init__(self, repo: SymptomRepository = Depends(SymptomRepository)):
        self._repo = repo

    async def action(self, *args, **kwargs):
        data: SymptomCreate = args[0]
        created = await self._repo.create(self._repo.document_class(**data.dict()))
        return {"success": True, "data": created}


class ListSymptomsUC(UseCase):
    def __init__(self, repo: SymptomRepository = Depends(SymptomRepository)):
        self._repo = repo

    async def action(self, *args, **kwargs):
        skip = kwargs.get("skip", 0)
        limit = kwargs.get("limit", 100)
        paged = await self._repo.get_all(skip=skip, limit=limit)
        return {"success": True, "data": paged.data}


class GetSymptomUC(UseCase):
    def __init__(self, repo: SymptomRepository = Depends(SymptomRepository)):
        self._repo = repo

    async def action(self, *args, **kwargs):
        id: str = args[0]
        obj = await self._repo.get(id)
        return {"success": True, "data": obj}


class UpdateSymptomUC(UseCase):
    def __init__(self, repo: SymptomRepository = Depends(SymptomRepository)):
        self._repo = repo

    async def action(self, *args, **kwargs):
        id: str = args[0]
        data: SymptomUpdate = args[1]
        obj = await self._repo.get(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(obj, k, v)
        saved = await self._repo.update(obj)
        return {"success": True, "data": saved}


class DeleteSymptomUC(UseCase):
    def __init__(self, repo: SymptomRepository = Depends(SymptomRepository)):
        self._repo = repo

    async def action(self, *args, **kwargs):
        id: str = args[0]
        obj = await self._repo.get(id)
        await self._repo.delete(obj)
        return {"success": True, "message": "Symptom deleted successfully"}
