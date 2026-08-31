"""
RecoverAI — LangGraph Workflow Definition
"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agent.state import RecoveryState
from agent.nodes.detector import detect
from agent.nodes.diagnoser import diagnose
from agent.nodes.interventor import intervene
from agent.nodes.executor import execute
from agent.nodes.verifier import verify
from agent.nodes.reporter import report

def _route_after_detection(state: dict) -> str:
    if state.get("is_recoverable", True):
        return "diagnose"
    return "report"

def _route_after_verification(state: dict) -> str:
    recovery_status = state.get("recovery_status", "")
    if recovery_status in ["recovered", "escalated", "failed"]:
        return "report"
    if state.get("should_retry", False):
        return "diagnose"
    return "report"

def build_graph():
    builder = StateGraph(RecoveryState)
    builder.add_node("detect", detect)
    builder.add_node("diagnose", diagnose)
    builder.add_node("intervene", intervene)
    builder.add_node("execute", execute)
    builder.add_node("verify", verify)
    builder.add_node("report", report)
    
    builder.add_edge(START, "detect")
    builder.add_conditional_edges("detect", _route_after_detection, {"diagnose": "diagnose", "report": "report"})
    builder.add_edge("diagnose", "intervene")
    builder.add_edge("intervene", "execute")
    builder.add_edge("execute", "verify")
    builder.add_conditional_edges("verify", _route_after_verification, {"diagnose": "diagnose", "report": "report"})
    builder.add_edge("report", END)
    
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)

recovery_agent = build_graph()
