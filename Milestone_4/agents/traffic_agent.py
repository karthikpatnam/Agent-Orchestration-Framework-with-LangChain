"""Traffic Intelligence Agent - Analyzes traffic conditions"""
from typing import Dict, Any
from models_pkg.schemas import RouteOptimizationState  # type: ignore
from api.clients import fetch_traffic_intelligence  # type: ignore

async def traffic_intelligence_agent(state: RouteOptimizationState) -> Dict[str, Any]:
    """Analyze traffic congestion and predict delays"""
    lon, lat = state["dest_coords"]
    risk = await fetch_traffic_intelligence([lon, lat], [lon, lat])
    
    report = f"Predicted path congestion base level: {risk}%"
    
    return {
        "traffic_report": report,
        "traffic_score": risk
    }
