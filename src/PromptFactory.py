import json
import logging
from utils.utils import generate_weather_data_summary

logger = logging.getLogger("prompt_factory")


class PromptFactory:
    prompt_templates = None

    def __init__(self, prompt_templates="data/prompt_templates.json"):
        with open(prompt_templates, 'r') as file:
            self.prompt_templates = json.load(file)

    def generate_prompt(self, weather_data, language, style, type, model="api"):

        data = {}
        prompt = self.prompt_templates[model][type][style]
        weather_data_summary = generate_weather_data_summary(weather_data)

        data["city"] = weather_data_summary[0].get("city", "Unknown")
        data["language"] = language
        data["weather_data"] = weather_data_summary

        prompt = prompt.format(**data)
        logger.debug(f"Generated prompt: {prompt}")

        return prompt
