"""
RecoverAI — Interventor Node (USES AI)
"""
from datetime import datetime

ALL_INTERVENTIONS = [
    "smart_retry", "send_payment_link", "request_card_update",
    "suggest_domestic_method", "send_recovery_email", "send_reactivation_offer",
    "delayed_retry", "send_invoice_reminder", "send_gentle_reminder", "escalate_manual"
]

def _parse_ai_response(text: str) -> tuple[str, str, list[str]]:
    lines = text.strip().split("\n")
    intervention = "send_payment_link"
    reasoning = "AI selected"
    alts = []
    for line in lines:
        if "INTERVENTION:" in line.upper():
            val = line.split(":", 1)[1].strip().lower()
            if val in ALL_INTERVENTIONS: intervention = val
        elif "REASONING:" in line.upper():
            reasoning = line.split(":", 1)[1].strip()
    return intervention, reasoning, alts

async def intervene(state: dict) -> dict:
    txn = state.get("transaction", {})
    txn_id = state.get("transaction_id", "UNKNOWN")
    failure_type = state.get("failure_type", "unknown")
    now = datetime.now().isoformat()
    
    intervention = "send_payment_link"
    reasoning = "Fallback selected"
    method = "rule_based"
    fallback_used = False

    try:
        from agent.llm import get_llm
        llm = get_llm()
        if llm:
            prompt = f"Pick one intervention for {failure_type} from {ALL_INTERVENTIONS}. Format:\nINTERVENTION: name\nREASONING: why"
            response = await llm.ainvoke(prompt)
            intervention, reasoning, _ = _parse_ai_response(response.content)
            method = "ai"
        else:
            raise ValueError("No LLM")
    except Exception:
        fallback_used = True

    audit_entry = {
        "timestamp": now,
        "node": "interventor",
        "action": "selected_intervention",
        "details": f"Action: {intervention} | Method: {method}",
        "ai_used": method == "ai",
        "confidence": 0.85 if method == "ai" else 0.70,
        "fallback": fallback_used,
    }

    return {
        "intervention": intervention,
        "intervention_reasoning": reasoning,
        "intervention_method": method,
        "alternative_interventions": [],
        "audit_log": [audit_entry],
    }
