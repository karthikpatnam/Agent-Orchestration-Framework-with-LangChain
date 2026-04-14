"""Risk Aggregator Node - Combines risk scores from all agents"""
from typing import Dict, Any
from models_pkg.schemas import RouteOptimizationState  # type: ignore

async def risk_aggregator_node(state: RouteOptimizationState) -> Dict[str, Any]:
    """Aggregate risk scores from all intelligence agents"""
    w_score = state.get("weather_score", 0.0)
    n_score = state.get("news_score", 0.0)
    t_score = state.get("traffic_score", 0.0)
    
    updated_routes = []
    original_route = state["routes"][0] if state["routes"] else None
    
    for r in state["routes"]:
        r.weather_risk_score = w_score
        r.news_risk_score = n_score
        r_traffic = min(100.0, t_score * (r.duration_s / 3600.0))
        r.traffic_risk_score = r_traffic
        
        # Calculate total cost
        cost = (r.distance_m / 1000) * 0.15 + (r.duration_s / 60) * 0.5
        r.cost = round(cost, 2)
        
        # Weighted score calculation
        r.total_score = round(
            r.cost + 
            (w_score * 0.5) + 
            (n_score * 3.0) + 
            (r_traffic * 0.5), 
            2
        )
        
        # Mark dangerous routes
        if n_score > 40.0 or w_score > 70.0 or r.total_score > 500:
            r.is_dangerous = True
            
        updated_routes.append(r)
        
    return {"routes": updated_routes, "original_route": original_route}
