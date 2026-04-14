"""Route Generator Agent - Fetches candidate routes between coordinates"""
from typing import Dict, Any
from models_pkg.schemas import RouteOptimizationState, RouteInfo  # type: ignore
from api.clients import fetch_routes  # type: ignore
import uuid

async def route_generator(state: RouteOptimizationState) -> Dict[str, Any]:
    """Generate alternative routes between source and destination"""
    data = await fetch_routes(state["source_coords"], state["dest_coords"])
    routes = []
    
    features = data.get("routes", data.get("features", []))
    for r in features:
        summary = r.get("summary", {})
        routes.append(RouteInfo(
            id=f"route-{str(uuid.uuid4().hex)[0:8]}",
            geometry=str(r.get("geometry", "")),
            distance_m=summary.get("distance", 0.0),
            duration_s=summary.get("duration", 0.0)
        ))
    
    if not routes:
        routes.append(RouteInfo(id="fallback", geometry="", distance_m=1000, duration_s=100))
        
    return {"routes": routes, "iterations": state.get("iterations", 0) + 1}
