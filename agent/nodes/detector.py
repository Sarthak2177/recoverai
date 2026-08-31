"""
RecoverAI — Detector Node (NO AI)
"""
from datetime import datetime

def detect(state: dict) -> dict:
    txn = state.get("transaction", {})
    txn_id = txn.get("id", "UNKNOWN")
    now = datetime.now().isoformat()
    
    validation_errors = []
    for field in ["id", "type", "amount", "currency", "failure_reason", "customer"]:
        if field not in txn or txn[field] is None:
            validation_errors.append(f"Missing required field: {field}")
            
    amount = txn.get("amount", 0)
    if not isinstance(amount, (int, float)) or amount <= 0:
        validation_errors.append(f"Invalid amount: {amount}")
        
    failure_type = txn.get("type", "unknown")
    if failure_type not in ["payment_failure", "checkout_abandonment", "subscription_lapse", "overdue_invoice"]:
        validation_errors.append(f"Unknown failure type: {failure_type}")
        failure_type = "unknown"
        
    failure_reason = txn.get("failure_reason", {})
    is_recoverable = failure_reason.get("recoverable", True) if isinstance(failure_reason, dict) else True
    if len(validation_errors) > 2:
        is_recoverable = False
        
    customer = txn.get("customer", {})
    dnd_enabled = customer.get("dnd_enabled", False)
    current_hour = datetime.now().hour
    contact_window_ok = 9 <= current_hour <= 21

    audit_entry = {
        "timestamp": now,
        "node": "detector",
        "action": "classified_transaction",
        "details": f"Transaction {txn_id}: {failure_type} | Amount: ₹{amount:,.2f} | Recoverable: {is_recoverable} | Validation issues: {len(validation_errors)}",
        "ai_used": False,
        "confidence": 1.0,
        "fallback": False,
    }

    return {
        "transaction_id": txn_id,
        "failure_type": failure_type,
        "is_recoverable": is_recoverable,
        "validation_errors": validation_errors,
        "contact_window_ok": contact_window_ok,
        "dnd_respected": dnd_enabled,
        "recovery_status": "pending" if is_recoverable else "skipped",
        "attempt_count": 0,
        "max_attempts": 3,
        "amount_recovered": 0.0,
        "compliance_flags": ["DND_ENABLED"] if dnd_enabled else [],
        "audit_log": [audit_entry],
    }
