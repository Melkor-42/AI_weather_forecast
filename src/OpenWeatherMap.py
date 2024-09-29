import httpx
import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("OpenWeatherMap")


class OpenWeatherMap:
    _instance = None
    _client: Optional[httpx.AsyncClient] = None

    BASE_URL = "http://api.openweathermap.org"

    def __new__(cls, api_key: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(OpenWeatherMap, cls).__new__(cls)
            cls._client = httpx.AsyncClient()  # Create client instance
        return cls._instance

    def __init__(self, api_key: Optional[str] = None):
        if not hasattr(self, 'initialized'):  # Ensure __init__ only runs once
            self.api_key = api_key or os.getenv("OPEN_WEATHER_TOKEN")
            if not self.api_key:
                raise ValueError("API Key for OpenWeatherMap is required.")
            self.initialized = True

    async def get_geolocation(self, city: str, limit: int = 5) -> Dict[str, Any]:

        url = f"{self.BASE_URL}/geo/1.0/direct"
        params = {
            "q": city,
            "limit": limit,
            "appid": self.api_key,
        }

        response = await self._client.get(url, params=params)
        response.raise_for_status()  # Handle non-200 responses
        data = response.json()
        if not data:
            raise ValueError("City not found.")
        return data

    async def get_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:

        logger.debug(f"Get current weather lat: {lat} lon: {lon}")
        url = f"{self.BASE_URL}/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }

        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # Max cnt in free version is 40
    async def get_daily_weather_forecast(self, lat: float, lon: float, cnt: int = 40) -> Dict[str, Any]:

        logger.debug(f"Get daily weather forecast lat: {lat} lon: {lon}")
        url = f"{self.BASE_URL}/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "cnt": cnt
        }

        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def get_historical_weather_data(self, lat: float, lon: float, start_date: str, hours: int = 24) -> Dict[str, Any]:


        url = f"{self.BASE_URL}/data/2.5/history/city"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "type": "hour",
            "cnt": hours
        }

        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self):
        if self._client:
            await self._client.aclose()
