"""News Intelligence Agent - Analyzes geopolitical news and disruptions using Google Gemini"""
from typing import Dict, Any
import json
import asyncio
from models_pkg.schemas import RouteOptimizationState  # type: ignore
from api.clients import fetch_geopolitical_news  # type: ignore
from config import settings  # type: ignore

async def news_intelligence_agent(state: RouteOptimizationState) -> Dict[str, Any]:
    """Analyze geopolitical news and risks using Google Gemini API"""
    lon, lat = state["dest_coords"]
    
    # Fetch news in thread to avoid blocking
    news_text = await asyncio.to_thread(fetch_geopolitical_news, lon, lat)
    
    try:
        # Use Google Gemini API instead of OpenAI
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Analyze the following recent news for geopolitical conflicts, road blockages, strikes, or major infrastructure delays.
Score the risk on a scale of 0 to 100, where 0 is no risk and 100 is impossible to travel safely.

News: {news_text}

Provide response in valid JSON format: {{"risk_score": 50, "summary": "Brief explanation"}}
Return ONLY the JSON, no other text."""
        
        response = await asyncio.to_thread(model.generate_content, prompt)
        content = response.text.lower()
        
        # Parse JSON response
        data = json.loads(content)
        score = float(data.get("risk_score", 0))
        report = data.get("summary", "No news issues.")
        
    except Exception as e:
        print(f"Google Gemini/JSON Error: {e}")
        score = 0.0
        report = "Failed to analyze news (API limit/error). Using heuristic analysis."
        
        # Fallback heuristic analysis
        if "conflict" in news_text.lower() or "block" in news_text.lower():
            score = 85.0
            report = "[Heuristic Override]: News contains critical disruption keywords - HIGH RISK."
    
    return {"news_report": report, "news_score": score}
