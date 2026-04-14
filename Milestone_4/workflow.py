from langgraph.graph import StateGraph, START, END  # type: ignore
from models import RouteOptimizationState  # type: ignore
from nodes import (  # type: ignore
    route_generator, weather_prediction_agent, news_intelligence_agent, traffic_intelligence_agent,
    risk_aggregator_node, decision_engine, explanation_node, monitor_node
)

def create_workflow():
    workflow = StateGraph(RouteOptimizationState)
    
    workflow.add_node("route_generator", route_generator)
    workflow.add_node("weather_prediction_agent", weather_prediction_agent)
    workflow.add_node("news_intelligence_agent", news_intelligence_agent)
    workflow.add_node("traffic_intelligence_agent", traffic_intelligence_agent)
    workflow.add_node("risk_aggregator_node", risk_aggregator_node)
    workflow.add_node("decision_engine", decision_engine)
    workflow.add_node("explanation_node", explanation_node)
    workflow.add_node("monitor_node", monitor_node)
    
    # Start
    workflow.add_edge(START, "route_generator")
    
    # Parallel fan-out
    workflow.add_edge("route_generator", "weather_prediction_agent")
    workflow.add_edge("route_generator", "news_intelligence_agent")
    workflow.add_edge("route_generator", "traffic_intelligence_agent")
    
    # Parallel fan-in
    workflow.add_edge("weather_prediction_agent", "risk_aggregator_node")
    workflow.add_edge("news_intelligence_agent", "risk_aggregator_node")
    workflow.add_edge("traffic_intelligence_agent", "risk_aggregator_node")
    
    # Rest of pipeline
    workflow.add_edge("risk_aggregator_node", "decision_engine")
    workflow.add_edge("decision_engine", "explanation_node")
    workflow.add_edge("explanation_node", "monitor_node")
    
    def reroute_decision(state: RouteOptimizationState):
        if state.get("reroute_needed", False):
            return "route_generator"
        return END

    workflow.add_conditional_edges("monitor_node", reroute_decision)
    
    return workflow.compile()

app_workflow = create_workflow()
