from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class GuardrailStatus(str, Enum):
    APPROVED = "approved"
    MODIFIED = "modified"
    BLOCKED = "blocked"


class SafetyIssueType(str, Enum):
    UNSAFE_PHYSICAL_ACTION = "unsafe_physical_action"
    INAPPROPRIATE_LANGUAGE = "inappropriate_language"
    CLINICAL_CONTRADICTION = "clinical_contradiction"
    HALLUCINATION_DETECTED = "hallucination_detected"
    ESCALATION_REQUIRED = "escalation_required"


class GuardrailVerdict(BaseModel):
    event_id: str
    trace_id: str
    checked_at: datetime = Field(default_factory=datetime.now)
    status: GuardrailStatus
    issues_found: list[SafetyIssueType] = []
    explanation: Optional[str] = None
    original_speech_text: Optional[str] = None
    modified_speech_text: Optional[str] = None
    guardrail_confidence: float = Field(
        default=1.0, ge=0.0, le=1.0
    )

    class Config:
        use_enum_values = True