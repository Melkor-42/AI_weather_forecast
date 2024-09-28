from pydantic import BaseModel, Field
from typing import Literal, List


class ArticleRequest(BaseModel):
    lat: float
    lon: float
    style: Literal['factual', 'tabloid', 'concise'] = Field("factual", description="Article style (factual, tabloid or concise)")
    language: Literal['SK', 'EN'] = Field("English", description="Article language ('SK' or 'EN')")


class ForecastArticleRequest(BaseModel):
    lat: float
    lon: float
    style: Literal['factual', 'tabloid', 'concise'] = Field("factual", description="Article style (factual, tabloid or concise)")
    language: Literal['SK', 'EN'] = Field("English", description="Article language ('SK' or 'EN')")


class LocalArticleRequest(BaseModel):
    lat: float
    lon: float
    style: Literal['factual'] = Field("factual", description="Article style (factual)")
    language: Literal['EN'] = Field("English", description="Article language ('SK' or 'EN')")


class ArticleResponse(BaseModel):
    headline: str
    lead: str
    body: str


class CoordinatesResponse(BaseModel):
    lat: float
    lon: float

class CitySuggestion(BaseModel):
    name: str
    country: str

class CitySuggestionsResponse(BaseModel):
    suggestions: List[CitySuggestion]