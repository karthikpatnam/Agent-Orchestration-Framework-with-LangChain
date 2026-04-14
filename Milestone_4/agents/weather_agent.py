"""Weather Prediction Agent - Analyzes weather conditions and risk"""
from typing import Dict, Any
from models_pkg.schemas import RouteOptimizationState  # type: ignore
from api.clients import fetch_weather_risk  # type: ignore

async def weather_prediction_agent(state: RouteOptimizationState) -> Dict[str, Any]:
    """Analyze weather conditions at destination"""
    lon, lat = state["dest_coords"]
    risk = await fetch_weather_risk(lon, lat)
    
    if risk < 20:
        report = "Clear weather conditions - no significant weather risks."
    elif risk < 50:
        report = "Moderate weather disruption potential - exercise caution."
    else:
        report = "High weather risk detected - severe conditions ahead."
    
    return {"weather_report": report, "weather_score": risk}
