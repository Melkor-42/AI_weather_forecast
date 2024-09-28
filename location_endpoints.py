from fastapi import APIRouter, HTTPException
from src.OpenWeatherMap import OpenWeatherMap
from models.pydantic_models import CoordinatesResponse, CitySuggestionsResponse

router = APIRouter()


@router.get("/location/cities", response_model=CitySuggestionsResponse)
async def get_cities(query: str):

    open_weather_client = OpenWeatherMap()
    try:
        data = await open_weather_client.get_geolocation(query)
        cities = [{"name": item['name'], "country": item['country']} for item in data]
        return {"suggestions": cities}
    except Exception as err:
        return {"error": str(err)}


@router.get("/location/coordinates", response_model=CoordinatesResponse)
async def get_coordinates(city: str, country: str):

    open_weather_client = OpenWeatherMap()
    try:
        data = await open_weather_client.get_geolocation(city=f"{city},{country}", limit=1)
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return {"lat": lat, "lon": lon}
        else:
            raise HTTPException(status_code=404, detail="City not found")
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))