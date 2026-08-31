"""
RecoverAI — Reporter Node (NO AI)
"""
from datetime import datetime

def report(state: dict) -> dict:
    recovery_status = state.get("recovery_status", "unknown")
    amount_recovered = state.get("amount_recovered", 0.0)
    stop_reason = state.get("stop_reason", "")
    now = datetime.now().isoformat()
    
    if recovery_status == "skipped":
         summary = f"Transaction skipped."
    elif recovery_status == "recovered":
         summary = f"Successfully recovered INR {amount_recovered:,.2f}."
    else:
         summary = f"Recovery failed/escalated. Reason: {stop_reason}"

    audit_entry = {
        "timestamp": now,
        "node": "reporter",
        "action": "finalized_report",
        "details": f"Final Status: {recovery_status.upper()} | {summary}",
        "ai_used": False,
        "confidence": 1.0,
        "fallback": False,
    }

    return {
        "audit_log": [audit_entry],
    }
