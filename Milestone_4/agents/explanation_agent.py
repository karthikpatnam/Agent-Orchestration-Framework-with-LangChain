"""Explanation Node - Generates human-readable explanations using Google Gemini"""
from typing import Dict, Any
import asyncio
from models_pkg.schemas import RouteOptimizationState  # type: ignore
from config import settings  # type: ignore

async def explanation_node(state: RouteOptimizationState) -> Dict[str, Any]:
    """Generate explanation for route selection using Google Gemini"""
    best = state.get("best_route")
    
    if not best:
        return {"explanation": "No suitable route found."}
    
    try:
        # Use Google Gemini API to generate explanation
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Based on the following route analysis data, explain why this route was recommended:

Route ID: {best.id}
Distance: {best.distance_m}m
Duration: {best.duration_s}s
Weather Risk Score: {best.weather_risk_score}
News Risk Score: {best.news_risk_score}
Traffic Risk Score: {best.traffic_risk_score}
Total Score: {best.total_score}
Is Dangerous: {best.is_dangerous}

Weather Report: {state.get('weather_report', 'N/A')}
News Report: {state.get('news_report', 'N/A')}
Traffic Report: {state.get('traffic_report', 'N/A')}

Provide a brief (2-3 sentences), professional explanation of why this route balances safety and speed."""
        
        response = await asyncio.to_thread(model.generate_content, prompt)
        explanation = response.text
        
    except Exception as e:
        print(f"Google Gemini Error: {e}")
        explanation = (
            f"Route {best.id} was selected by balancing distance ({best.distance_m}m), "
            f"duration ({best.duration_s}s), and risk factors (Weather: {best.weather_risk_score}, "
            f"News: {best.news_risk_score}, Traffic: {best.traffic_risk_score})."
        )
    
    return {"explanation": explanation}
