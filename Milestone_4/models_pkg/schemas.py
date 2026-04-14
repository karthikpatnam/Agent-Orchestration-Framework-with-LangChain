from typing import List, Optional, Any, Dict, TypedDict
from pydantic import BaseModel  # type: ignore

class RouteInfo(BaseModel):
    id: str
    geometry: str
    distance_m: float
    duration_s: float
    weather_risk_score: Optional[float] = None
    news_risk_score: Optional[float] = None
    traffic_risk_score: Optional[float] = None
    cost: Optional[float] = None
    total_score: Optional[float] = None
    is_dangerous: bool = False

class OptimizationRequest(BaseModel):
    source_coords: List[float] # [lon, lat]
    dest_coords: List[float]   # [lon, lat]

class OptimizationResponse(BaseModel):
    original_route_id: str
    is_original_dangerous: bool
    recommended_route_id: str
    explanation: str
    routes: List[RouteInfo]

class RouteOptimizationState(TypedDict):
    source_coords: List[float]
    dest_coords: List[float]
    routes: List[RouteInfo]
    best_route: Optional[RouteInfo]
    original_route: Optional[RouteInfo]
    explanation: str
    reroute_needed: bool
    iterations: int
    weather_report: str
    news_report: str
    traffic_report: str
    weather_score: float
    news_score: float
    traffic_score: float
