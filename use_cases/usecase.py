from abc import ABC, abstractmethod


class UseCase(ABC):

    @abstractmethod
    async def action(self, *args, **kwargs):
        pass
