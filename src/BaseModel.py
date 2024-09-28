from abc import ABC, abstractmethod


class BaseModel(ABC):

    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        pass
