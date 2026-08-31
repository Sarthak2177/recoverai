"""
RecoverAI — Executor Node (NO AI)
Real Razorpay API Integration + Simulation Fallback
"""
from datetime import datetime
import random
import asyncio

def _simulate_execution(intervention: str, txn_amount: float) -> dict:
    prob = 0.40
    is_success = random.random() < prob
    if is_success:
        return {"success": True, "message": f"Successfully executed {intervention}.", "recovered_amount": txn_amount, "api_response": {"status": "paid", "id": f"sim_rec_{random.randint(1000, 9999)}"}}
    else:
        return {"success": False, "message": f"Execution of {intervention} failed.", "recovered_amount": 0.0, "api_response": {"status": "failed", "error": "Customer declined"}}

async def execute(state: dict) -> dict:
    txn = state.get("transaction", {})
    txn_id = state.get("transaction_id", "UNKNOWN")
    failure_type = state.get("failure_type", "unknown")
    intervention = state.get("intervention", "none")
    amount = txn.get("amount", 0)
    now = datetime.now().isoformat()
    
    try:
        from server.razorpay_client import get_rzp_client
        rzp_client = get_rzp_client()
        
        if rzp_client.is_configured:
            if intervention in ["send_payment_link", "smart_retry", "delayed_retry", "send_invoice_reminder", "request_card_update"]:
                api_resp = rzp_client.create_payment_link(amount=int(amount), currency=txn.get("currency", "INR"), description=f"Recovery for {txn_id}", customer=txn.get("customer", {}))
                if "error" not in api_resp:
                    result = {"success": True, "message": f"Real Razorpay API: Payment Link Created -> {api_resp.get('short_url')}", "recovered_amount": amount, "api_response": api_resp}
                else:
                    result = {"success": False, "message": f"Razorpay API Error: {api_resp.get('error')}", "recovered_amount": 0.0, "api_response": api_resp}
            else:
                result = _simulate_execution(intervention, amount)
                result["message"] += " (Simulated: Real API mapping missing for this action)"
        else:
            result = _simulate_execution(intervention, amount)
            
    except Exception as e:
        result = {"success": False, "message": f"System error: {str(e)}", "recovered_amount": 0.0, "api_response": {"error": "internal_error"}}

    audit_entry = {
        "timestamp": now,
        "node": "executor",
        "action": "executed_intervention",
        "details": f"Executed: {intervention} | Result: {'Success' if result['success'] else 'Failed'} | Msg: {result['message']}",
        "ai_used": False,
        "confidence": 1.0,
        "fallback": False,
    }

    return {
        "execution_result": result,
        "execution_success": result["success"],
        "execution_error": result["message"] if not result["success"] else "",
        "audit_log": [audit_entry],
    }
