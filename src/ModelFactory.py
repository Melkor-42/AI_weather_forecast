from src.BaseModel import BaseModel
from src.LocalModel import LocalModel
from src.ReplicateModel import ReplicateModel
import logging

logger = logging.getLogger("ModelFactory")


class ModelFactory:
    @staticmethod
    async def create_model(model: str) -> BaseModel:
        logger.debug(f"Creating model: {model}")
        if model == 'flan-t5-large':
            return LocalModel(model)
        elif model == "meta/meta-llama-3.1-405b-instruct":
            return ReplicateModel(model)
        raise ValueError("Invalid LLM model")