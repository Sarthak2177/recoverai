"""
RecoverAI — Agent State Definition
"""
from typing import TypedDict, Literal, Annotated
import operator

class AuditEntry(TypedDict, total=False):
    timestamp: str
    node: str
    action: str
    details: str
    ai_used: bool
    confidence: float
    fallback: bool

class RecoveryState(TypedDict, total=False):
    transaction: dict
    transaction_id: str
    failure_type: str
    is_recoverable: bool
    validation_errors: list[str]
    root_cause: str
    diagnosis_confidence: float
    diagnosis_method: str
    contributing_factors: list[str]
    intervention: str
    intervention_reasoning: str
    intervention_method: str
    alternative_interventions: list[str]
    execution_result: dict
    execution_success: bool
    execution_error: str
    recovery_status: str
    amount_recovered: float
    attempt_count: int
    max_attempts: int
    should_retry: bool
    stop_reason: str
    compliance_flags: list[str]
    contact_window_ok: bool
    dnd_respected: bool
    audit_log: Annotated[list[dict], operator.add]
    error_details: str
    batch_id: str
