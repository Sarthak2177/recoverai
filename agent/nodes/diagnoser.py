"""
RecoverAI — Diagnoser Node (USES AI)
"""
from datetime import datetime

RULE_BASED_DIAGNOSES = {
    "CARD_DECLINED": "Card was declined by the issuing bank.",
    "INSUFFICIENT_FUNDS": "The customer's account does not have sufficient balance.",
    "NETWORK_ERROR": "The payment failed due to a network timeout.",
    "BANK_REFUSED": "The customer's bank has actively refused this transaction.",
    "EXPIRED_CARD": "The card on file has passed its expiration date.",
    "INTERNATIONAL_BLOCKED": "International transactions are not enabled on this card.",
    "INVALID_CVV": "The CVV entered does not match the card.",
    "3DS_FAILED": "3D Secure authentication failed.",
    "RISK_CHECK_FAILED": "The transaction was flagged by the payment risk engine.",
    "BANK_DOWNTIME": "The issuing bank's systems are currently unavailable.",
    "CART_BUILT": "Customer added items to cart but left before proceeding to checkout.",
    "ADDRESS_ENTERED": "Customer entered shipping address but didn't continue to payment.",
    "PAYMENT_PAGE": "Customer reached the payment page but didn't complete.",
    "OTP_PENDING": "Customer entered card details but abandoned at OTP verification.",
    "UPI_PENDING": "Customer selected UPI but didn't complete the payment flow.",
    "RECURRING_DECLINED": "The recurring charge was declined by the bank.",
    "CARD_EXPIRED_SUB": "The card linked to this subscription has expired.",
    "MANDATE_REVOKED": "The customer has actively revoked their UPI autopay mandate.",
    "INSUFFICIENT_FUNDS_SUB": "The customer's account lacks sufficient funds for renewal.",
    "ACCOUNT_CLOSED": "The bank account linked to this subscription has been closed.",
    "PAYMENT_METHOD_REMOVED": "The saved payment method is no longer valid.",
    "NOT_VIEWED": "The invoice has not been opened or viewed by the customer.",
    "DISPUTED": "The customer is disputing the invoice amount.",
    "PARTIAL_PAYMENT": "The customer made a partial payment, leaving a balance.",
    "PAYMENT_PENDING": "The customer has acknowledged the invoice but payment is pending.",
    "CONTACT_UNREACHABLE": "Unable to reach the customer for invoice follow-up.",
}

async def diagnose(state: dict) -> dict:
    txn = state.get("transaction", {})
    txn_id = state.get("transaction_id", "UNKNOWN")
    failure_type = state.get("failure_type", "unknown")
    failure_reason = txn.get("failure_reason", {})
    failure_code = failure_reason.get("code", "UNKNOWN") if isinstance(failure_reason, dict) else "UNKNOWN"
    now = datetime.now().isoformat()
    
    diagnosis_method = "rule_based"
    fallback_used = False
    root_cause = ""
    confidence = 0.0
    contributing_factors = []

    try:
        from agent.llm import get_llm
        llm = get_llm()
        if llm:
            prompt = f"Diagnose this {failure_type} for ID {txn_id}. Code: {failure_code}. Describe root cause in 2 sentences."
            response = await llm.ainvoke(prompt)
            root_cause = response.content.strip()
            confidence = 0.95
            diagnosis_method = "ai"
        else:
            raise ValueError("No LLM")
    except Exception:
        root_cause = RULE_BASED_DIAGNOSES.get(failure_code, f"Failed: {failure_code}")
        confidence = 0.7
        fallback_used = True

    audit_entry = {
        "timestamp": now,
        "node": "diagnoser",
        "action": "diagnosed_root_cause",
        "details": f"Diagnosis: {root_cause[:100]}... | Method: {diagnosis_method}",
        "ai_used": diagnosis_method == "ai",
        "confidence": confidence,
        "fallback": fallback_used,
    }

    return {
        "root_cause": root_cause,
        "diagnosis_confidence": confidence,
        "diagnosis_method": diagnosis_method,
        "contributing_factors": contributing_factors,
        "recovery_status": "recovering",
        "audit_log": [audit_entry],
    }
