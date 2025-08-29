from abc import ABC
from typing import Generic, TypeVar, Type

from app.errors.not_found import NotFoundException
from app.models.base import Base

T = TypeVar("T", bound=Base)


class PaginatedData(Generic[T]):
    def __init__(self, data: list[T]):
        self.data = data


class Repository(ABC, Generic[T]):
    document_class: Type[T]

    async def get(self, id: str) -> T:
        document = await self.document_class.get(id)
        if not document:
            raise NotFoundException("Document not found", id)
        return document

    async def get_all(self) -> list[T]:
        document_list = await self.document_class.find_all().to_list()
        return document_list

    async def create(self, data: T) -> T:
        return await self.document_class.insert(data)

    async def update(self, data: T) -> T:
        return await data.save()

    async def delete(self, obj: T) -> None:
        await obj.delete()

    async def delete_by_id(self, id: str) -> None:
        await (await self.document_class.get(id)).delete()


class PaginatedRepository(Repository[T], Generic[T]):
    async def get_all(self, skip: int = 0, limit: int = 100) -> PaginatedData[T]:
        document_list = await self.document_class.find_all().skip(skip).limit(limit).to_list()
        return PaginatedData(document_list)
