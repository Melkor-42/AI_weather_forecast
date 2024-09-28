from src.BaseModel import BaseModel
import replicate
from replicate.exceptions import ModelError
import json
import logging

logger = logging.getLogger("ReplicateModel")


class ReplicateModel(BaseModel):
    def __init__(self, model_name: str):
        self.model = replicate.models.get(model_name)

    async def generate_text(self, prompt: str):
        try:
            output = await replicate.async_run(
                self.model,
                input={
                    "top_k": 50,
                    "top_p": 0.9,
                    "prompt": prompt,
                    "max_tokens": 1024,
                    "min_tokens": 0,
                    "temperature": 0.1,
                    "system_prompt": "You are weather forecast reporter.",
                    "presence_penalty": 0.1,
                    "frequency_penalty": 0.1
                },
            )
        except ModelError as err:
            logger.error(f"Failed prediction: {err}")
            raise Exception("Failed to generate text.")

        json_output = await self.__parse_weather_data(output)
        return json_output

    async def __parse_weather_data(self, token_array):
        text = ''.join(token_array).strip()

        start_head = text.find('**')
        end_head = text.find('**', start_head + 2)
        head = text[start_head + 2:end_head].strip()

        start_lead = text.find('**', end_head + 2)
        end_lead = text.find('**', start_lead + 2)
        lead = text[start_lead + 2:end_lead].strip()

        body = text[end_lead + 2:].strip()

        weather_report = {
            "head": head,
            "lead": lead,
            "body": body
        }

        return weather_report
