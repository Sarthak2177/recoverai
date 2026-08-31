"""
RecoverAI — Verifier Node (NO AI)
"""
from datetime import datetime

def verify(state: dict) -> dict:
    txn_id = state.get("transaction_id", "UNKNOWN")
    execution_success = state.get("execution_success", False)
    execution_result = state.get("execution_result", {})
    attempt_count = state.get("attempt_count", 0) + 1
    max_attempts = state.get("max_attempts", 3)
    now = datetime.now().isoformat()
    
    should_retry = False
    stop_reason = ""
    recovery_status = state.get("recovery_status", "pending")
    amount_recovered = 0.0
    
    if execution_success:
        recovery_status = "recovered"
        amount_recovered = execution_result.get("recovered_amount", 0.0)
        stop_reason = "recovery_successful"
    else:
        api_error = execution_result.get("api_response", {}).get("error", "")
        if "declined" in str(api_error).lower():
            should_retry = False
            stop_reason = "customer_explicit_decline"
            recovery_status = "escalated"
        elif attempt_count >= max_attempts:
            should_retry = False
            stop_reason = "max_attempts_reached"
            recovery_status = "failed"
        elif not state.get("contact_window_ok", True):
             should_retry = False
             stop_reason = "outside_contact_window"
             recovery_status = "escalated"
        else:
            should_retry = True
            stop_reason = ""
            recovery_status = "recovering"
            
    audit_entry = {
        "timestamp": now,
        "node": "verifier",
        "action": "verified_execution",
        "details": f"Attempt {attempt_count}/{max_attempts} | Next: {'Retry' if should_retry else 'Stop'}",
        "ai_used": False,
        "confidence": 1.0,
        "fallback": False,
    }

    return {
        "recovery_status": recovery_status,
        "attempt_count": attempt_count,
        "should_retry": should_retry,
        "stop_reason": stop_reason,
        "amount_recovered": amount_recovered,
        "audit_log": [audit_entry],
    }
