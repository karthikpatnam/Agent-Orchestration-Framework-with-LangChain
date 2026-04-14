"""Monitor Node - Evaluates if rerouting is needed"""
from typing import Dict, Any
from models_pkg.schemas import RouteOptimizationState  # type: ignore

async def monitor_node(state: RouteOptimizationState) -> Dict[str, Any]:
    """Monitor route viability and decide if rerouting is needed"""
    best = state.get("best_route")
    iterations = state.get("iterations", 0)
    
    # Reroute if best route is too dangerous and we haven't exceeded iterations
    reroute_needed = False
    if best and best.is_dangerous and iterations < 2:
        reroute_needed = True
    
    return {"reroute_needed": reroute_needed}
