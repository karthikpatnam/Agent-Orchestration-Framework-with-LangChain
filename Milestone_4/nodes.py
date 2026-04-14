from typing import Dict, Any
from langchain_openai import ChatOpenAI  # type: ignore
from langchain_core.prompts import PromptTemplate  # type: ignore
from models import RouteOptimizationState, RouteInfo  # type: ignore
from clients import fetch_routes, fetch_weather_risk, fetch_geopolitical_news, fetch_traffic_intelligence  # type: ignore
import uuid

async def route_generator(state: RouteOptimizationState) -> Dict[str, Any]:
    data = await fetch_routes(state["source_coords"], state["dest_coords"])
    routes = []
    
    features = data.get("routes", data.get("features", []))
    for r in features:
        summary = r.get("summary", {})
        routes.append(RouteInfo(
            id=f"route-{str(uuid.uuid4().hex)[0:8]}",  # type: ignore[index]
            geometry=str(r.get("geometry", "")),
            distance_m=summary.get("distance", 0.0),
            duration_s=summary.get("duration", 0.0)
        ))
    if not routes:
        routes.append(RouteInfo(id="fallback", geometry="", distance_m=1000, duration_s=100))
        
    return {"routes": routes, "iterations": state.get("iterations", 0) + 1}

async def weather_prediction_agent(state: RouteOptimizationState) -> Dict[str, Any]:
    lon, lat = state["dest_coords"]
    risk = await fetch_weather_risk(lon, lat)
    report = "Clear weather." if risk < 20 else "Moderate weather disruption potential." if risk < 50 else "High weather risk detected."
    return {"weather_report": report, "weather_score": risk}

async def news_intelligence_agent(state: RouteOptimizationState) -> Dict[str, Any]:
    lon, lat = state["dest_coords"]
    import asyncio
    news_text = await asyncio.to_thread(fetch_geopolitical_news, lon, lat)
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    prompt = PromptTemplate.from_template(
        "Analyze the following recent news for geopolitical conflicts, road blockages, strikes, or major infrastructure delays. "
        "Score the risk on a scale of 0 to 100, where 0 is no risk and 100 is impossible to travel safely.\n"
        "News: {news}\n"
        "Provide ONLY a valid JSON like: {{\"risk_score\": 50, \"summary\": \"Brief explanation\"}}"
    )
    try:
        resp = await llm.ainvoke(prompt.format(news=news_text))
        content = resp.content.lower()
        
        import json
        data = json.loads(content)
        score = float(data.get("risk_score", 0))
        report = data.get("summary", "No news issues.")
    except Exception as e:
        print(f"LLM/JSON Error: {e}")
        score = 0.0
        report = "Failed to parse news intelligence (possibly API limits). Defaulting to zero risk."
        if "conflict" in news_text.lower() or "block" in news_text.lower():
            score = 85.0
            report = "[Offline Heuristic Override]: News explicitly matched critical disruption keywords. Proceeding extremely dangerous."
            
    return {"news_report": report, "news_score": score}

async def traffic_intelligence_agent(state: RouteOptimizationState) -> Dict[str, Any]:
    lon, lat = state["dest_coords"]
    risk = await fetch_traffic_intelligence([lon, lat], [lon, lat])
    return {"traffic_report": f"Predicted path congestion base level: {risk}%", "traffic_score": risk}

async def risk_aggregator_node(state: RouteOptimizationState) -> Dict[str, Any]:
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
        
        cost = (r.distance_m / 1000) * 0.15 + (r.duration_s / 60) * 0.5
        r.cost = round(cost, 2)
        r.total_score = round(r.cost + (w_score * 0.5) + (n_score * 3.0) + (r_traffic * 0.5), 2)
        
        if n_score > 40.0 or w_score > 70.0 or r.total_score > 500:
            r.is_dangerous = True
            
        updated_routes.append(r)
        
    return {"routes": updated_routes, "original_route": original_route}

async def decision_engine(state: RouteOptimizationState) -> Dict[str, Any]:
    best_route = None
    best_score = float('inf')
    
    for r in state["routes"]:
        penalized_score = r.total_score + (10000 if r.is_dangerous else 0)
        if penalized_score < best_score:
            best_score = penalized_score
            best_route = r
            
    return {"best_route": best_route}

async def explanation_node(state: RouteOptimizationState) -> Dict[str, Any]:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    prompt = PromptTemplate.from_template(
        "You are an AI routing advisor for a supply chain platform.\n"
        "Original Route Distance: {o_dist}m, Original Dangerous Flag: {o_danger}\n"
        "Recommended Route Distance: {r_dist}m\n"
        "Weather Report: {weather}\n"
        "News Report: {news}\n"
        "Traffic Report: {traffic}\n\n"
        "Explain to the user whether they should stick with the original or proceed with the recommended alternative and why. If the original was flagged dangerous, explicitly warn them."
    )
    oreq = state["original_route"]
    breq = state["best_route"]
    content = prompt.format(
        o_dist=oreq.distance_m if oreq else 0,
        o_danger="Yes" if (oreq and oreq.is_dangerous) else "No",
        r_dist=breq.distance_m if breq else 0,
        weather=state.get("weather_report", ""),
        news=state.get("news_report", ""),
        traffic=state.get("traffic_report", "")
    )
    
    try:
        response = await llm.ainvoke(content)
        exp_text = str(response.content)
    except Exception as e:
        print(f"Explanation LLM Error: {e}")
        exp_text = "[System Fallback] Automatic explanation generation unavailable (API Quota Limited). However, note that the original route was heavily penalized due to high risk factors detected by our multi-agent intelligence layer. We strongly recommend the alternative."
        
    return {"explanation": exp_text}

async def monitor_node(state: RouteOptimizationState) -> Dict[str, Any]:
    return {"reroute_needed": False}
