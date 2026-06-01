from langgraph.graph import StateGraph, END
from app.schemas.agent_state import AgentState, RoutingDecision
from app.agents.classifier import run_classifier
from app.agents.fast_trigger import run_fast_trigger


def route_after_classifier(state: AgentState) -> str:
    decision = state.routing_decision
    if decision == RoutingDecision.FAST_TRIGGER:
        return "fast_trigger"
    elif decision == RoutingDecision.MLLM_REASONER:
        print("[GRAPH] MLLM requested → fast_trigger stub")
        return "fast_trigger"
    elif decision == RoutingDecision.THERAPIST_REMINDER:
        print("[GRAPH] THERAPIST requested → discard stub")
        return "end_discard"
    else:
        return "end_discard"


def discard_event(state: AgentState) -> AgentState:
    print(f"[GRAPH] Discarded: {state.sensor_event.event_id}")
    return state


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("classifier", run_classifier)
    graph.add_node("fast_trigger", run_fast_trigger)
    graph.add_node("end_discard", discard_event)
    graph.set_entry_point("classifier")
    graph.add_conditional_edges(
        "classifier",
        route_after_classifier,
        {
            "fast_trigger": "fast_trigger",
            "end_discard": "end_discard"
        }
    )
    graph.add_edge("fast_trigger", END)
    graph.add_edge("end_discard", END)
    compiled = graph.compile()
    print("[GRAPH] Pipeline compiled successfully")
    return compiled


pipeline = build_graph()