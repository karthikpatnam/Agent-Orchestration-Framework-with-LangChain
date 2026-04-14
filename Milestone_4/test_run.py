import asyncio
from models import OptimizationRequest  # type: ignore
from main import app_workflow  # type: ignore
import traceback

async def main():
    initial_state = {
        "source_coords": [80.5586, 16.4300],
        "dest_coords": [80.5650, 16.4285],
        "routes": [],
        "best_route": None,
        "original_route": None,
        "explanation": "",
        "reroute_needed": False,
        "iterations": 0
    }
    print("Invoking LangGraph Multi-Agent workflow...")
    try:
        result = await app_workflow.ainvoke(initial_state)
        print("Success!\n")
        orig = result.get('original_route')
        best = result.get('best_route')
        
        if orig:
            print(f"Original Route: {orig.id} | Dangerous: {orig.is_dangerous}")
        if best:
            print(f"Recommended Route: {best.id}")
            
        print(f"\n--- Agents Reports ---")
        print(f"Weather: {result.get('weather_report')}")
        print(f"News (Geopolitical/Blockages): {result.get('news_report')}")
        print(f"Traffic: {result.get('traffic_report')}")
        
        print(f"\n--- LLM Explanation ---")
        print(result.get('explanation'))
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
