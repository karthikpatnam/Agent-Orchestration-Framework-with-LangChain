"""Decision Engine - Selects the optimal route"""
from typing import Dict, Any
from models_pkg.schemas import RouteOptimizationState  # type: ignore

async def decision_engine(state: RouteOptimizationState) -> Dict[str, Any]:
    """Select the best route based on aggregated risk scores"""
    best_route = None
    best_score = float('inf')
    
    for r in state["routes"]:
        # Penalize dangerous routes heavily
        penalized_score = r.total_score + (10000 if r.is_dangerous else 0)
        
        if penalized_score < best_score:
            best_score = penalized_score
            best_route = r
    
    if not best_route:
        best_route = state["routes"][0] if state["routes"] else None
        
    return {"best_route": best_route}
