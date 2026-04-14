from fastapi import FastAPI, HTTPException  # type: ignore
from fastapi.responses import HTMLResponse  # type: ignore
from models_pkg.schemas import OptimizationRequest, OptimizationResponse  # type: ignore
from core.workflow import app_workflow  # type: ignore
from ui_pkg.map_ui import get_map_ui  # type: ignore
from dotenv import load_dotenv  # type: ignore
import traceback

load_dotenv()

app = FastAPI(title="Multi-Agent Route Optimizer", version="2.0")

@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the interactive map UI"""
    return get_map_ui()

@app.get("/ui", response_class=HTMLResponse)
def ui():
    """Alternate UI endpoint"""
    return get_map_ui()

@app.post("/optimize-route", response_model=OptimizationResponse)
async def optimize_route(req: OptimizationRequest):
    """Optimize route considering weather, traffic, and geopolitical factors"""
    initial_state = {
        "source_coords": req.source_coords,
        "dest_coords": req.dest_coords,
        "routes": [],
        "best_route": None,
        "original_route": None,
        "explanation": "",
        "reroute_needed": False,
        "iterations": 0
    }
    try:
        result = await app_workflow.ainvoke(initial_state)
        
        best = result.get("best_route")
        orig = result.get("original_route")
        
        if not best or not orig:
            raise HTTPException(status_code=404, detail="No route found.")
            
        return OptimizationResponse(
            original_route_id=orig.id,
            is_original_dangerous=orig.is_dangerous,
            recommended_route_id=best.id,
            explanation=result["explanation"],
            routes=result["routes"]
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
def status():
    """Health check endpoint"""
    return {
        "status": "ok",
        "system": "Multi-Agent Route Optimizer",
        "version": "2.0"
    }
