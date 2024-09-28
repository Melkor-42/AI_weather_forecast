from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
from dotenv import load_dotenv

from middlewares.RequestControlMiddleware import RequestControlMiddleware
from middlewares.LogRequestMiddleware import LogRequestMiddleware
from location_endpoints import router as location_router
from models.pydantic_models import *
from utils.LogManager import setup_logger
from src.PromptFactory import PromptFactory
from src.ModelFactory import ModelFactory
from src.OpenWeatherMap import OpenWeatherMap

load_dotenv()
setup_logger()

templates = Jinja2Templates(directory="templates")
logger = logging.getLogger("ai_weather_forecast")

app = FastAPI()

app.add_middleware(RequestControlMiddleware)
app.add_middleware(LogRequestMiddleware)
app.include_router(location_router)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/articles/current/replicate", response_model=ArticleResponse)
async def generate_current_article_replicate(request: ArticleRequest):

    open_weather_client = OpenWeatherMap()
    weather_data = await open_weather_client.get_current_weather(lat=request.lat, lon=request.lon)
    factory = PromptFactory()
    prompt = factory.generate_prompt(weather_data, request.language, request.style, type="current")

    try:
        model = await ModelFactory.create_model("meta/meta-llama-3.1-405b-instruct")
        generated_text = await model.generate_text(prompt)
    except ValueError as err:
        raise HTTPException(status_code=500, detail=str(err))

    return ArticleResponse(headline=generated_text.get("head", "Current Weather"),
                           lead=generated_text.get("lead","Gather information about the current meteorological conditions."),
                           body=generated_text.get("body", "")
                           )


@app.post("/articles/current/local", response_model=ArticleResponse)
async def generate_current_article_local(request: LocalArticleRequest):

    open_weather_client = OpenWeatherMap()
    weather_data = await open_weather_client.get_current_weather(lat=request.lat, lon=request.lon)
    prompt_factory = PromptFactory()
    prompt = prompt_factory.generate_prompt(weather_data, request.language, request.style, type="current", model="local")

    try:
        model = await ModelFactory.create_model("flant-t5-large")
        generated_text = model.generate_text(prompt)
    except ValueError as err:
        raise HTTPException(status_code=500, detail=str(err))

    return ArticleResponse(headline="Current Weather", lead="Gather information about the current meteorological conditions.", body=generated_text)


@app.post("/articles/forecast", response_model=ArticleResponse)
async def generate_forecast_article(request: ForecastArticleRequest):

    open_weather_client = OpenWeatherMap()
    weather_data = await open_weather_client.get_daily_weather_forecast(lat=request.lat, lon=request.lon)
    factory = PromptFactory()
    prompt = factory.generate_prompt(weather_data, request.language, request.style, type="forecast")

    try:
        model = await ModelFactory.create_model("meta/meta-llama-3.1-405b-instruct")
        generated_text = await model.generate_text(prompt)
    except ValueError as err:
        raise HTTPException(status_code=500, detail=str(err))

    return ArticleResponse(headline=generated_text.get("head", "Weather forecast"),
                               lead=generated_text.get("lead", "Discover the weather forecast for the upcoming few days."),
                               body=generated_text.get("body", "")
                               )


if __name__ == "__main__":

    logger.info("Starting AI weather forecast.")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")