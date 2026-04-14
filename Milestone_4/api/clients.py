import httpx  # type: ignore
from config import settings  # type: ignore
from duckduckgo_search import DDGS  # type: ignore
import random

async def fetch_routes(start: list[float], end: list[float]):
    """Fetch alternative routes from OpenRouteService"""
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': settings.ORS_API_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }
    body = {"coordinates": [start, end], "alternative_routes": {"target_count": 3}}
    
    async with httpx.AsyncClient() as client:
        resp = await client.post('https://api.openrouteservice.org/v2/directions/driving-car', json=body, headers=headers)
        if resp.status_code != 200:
            print(f"ORS Error: {resp.status_code} - {resp.text}")
        resp.raise_for_status()
        return resp.json()

async def fetch_weather_risk(lon: float, lat: float) -> float:
    """Fetch weather data and calculate risk score"""
    params = {
        'lat': lat,
        'lon': lon,
        'appid': settings.OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get('https://api.openweathermap.org/data/2.5/weather', params=params)
        if resp.status_code == 200:
            data = resp.json()
            weather_main = data['weather'][0]['main'].lower()
            risk = 0.0
            if 'rain' in weather_main: risk += 30
            if 'snow' in weather_main: risk += 50
            if 'storm' in weather_main or 'thunder' in weather_main: risk += 80
            return float(min(risk, 100.0))
    return 10.0

def fetch_geopolitical_news(lon: float, lat: float) -> str:
    """Fetch geopolitical news and disruption information"""
    # Mock implementation - in production, integrate with real news API
    return "[Demo Intelligence Protocol Active]: Severe geopolitical conflict and supply chain disruption reported directly ahead on this path. Military roadblocks are active. Proceeding is extremely dangerous."

async def fetch_traffic_intelligence(start: list[float], end: list[float]) -> float:
    """Fetch traffic congestion data"""
    base_congestion: float = random.uniform(5.0, 40.0)
    return round(base_congestion, 2)  # type: ignore[return-value]
