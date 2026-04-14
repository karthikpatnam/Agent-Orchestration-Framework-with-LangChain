"""Main Workflow Orchestrator - Coordinates all agents using LangGraph"""
from langgraph.graph import StateGraph, START, END  # type: ignore
from models_pkg.schemas import RouteOptimizationState  # type: ignore
from agents.route_generator import route_generator  # type: ignore
from agents.weather_agent import weather_prediction_agent  # type: ignore
from agents.news_agent import news_intelligence_agent  # type: ignore
from agents.traffic_agent import traffic_intelligence_agent  # type: ignore
from agents.risk_aggregator import risk_aggregator_node  # type: ignore
from agents.decision_engine import decision_engine  # type: ignore
from agents.explanation_agent import explanation_node  # type: ignore
from agents.monitor_agent import monitor_node  # type: ignore

def create_workflow():
    """Create the route optimization workflow graph"""
    workflow = StateGraph(RouteOptimizationState)
    
    # Add all agent nodes
    workflow.add_node("route_generator", route_generator)
    workflow.add_node("weather_prediction_agent", weather_prediction_agent)
    workflow.add_node("news_intelligence_agent", news_intelligence_agent)
    workflow.add_node("traffic_intelligence_agent", traffic_intelligence_agent)
    workflow.add_node("risk_aggregator_node", risk_aggregator_node)
    workflow.add_node("decision_engine", decision_engine)
    workflow.add_node("explanation_node", explanation_node)
    workflow.add_node("monitor_node", monitor_node)
    
    # Define workflow edges
    # Start -> Route Generator
    workflow.add_edge(START, "route_generator")
    
    # Parallel fan-out: Route Generator -> All Risk Analysts
    workflow.add_edge("route_generator", "weather_prediction_agent")
    workflow.add_edge("route_generator", "news_intelligence_agent")
    workflow.add_edge("route_generator", "traffic_intelligence_agent")
    
    # Parallel fan-in: All Risk Analysts -> Risk Aggregator
    workflow.add_edge("weather_prediction_agent", "risk_aggregator_node")
    workflow.add_edge("news_intelligence_agent", "risk_aggregator_node")
    workflow.add_edge("traffic_intelligence_agent", "risk_aggregator_node")
    
    # Sequential pipeline
    workflow.add_edge("risk_aggregator_node", "decision_engine")
    workflow.add_edge("decision_engine", "explanation_node")
    workflow.add_edge("explanation_node", "monitor_node")
    
    # Conditional rerouting logic
    def reroute_decision(state: RouteOptimizationState):
        if state.get("reroute_needed", False):
            return "route_generator"
        return END

    workflow.add_conditional_edges("monitor_node", reroute_decision)
    
    return workflow.compile()

# Create the compiled workflow
app_workflow = create_workflow()
