from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from app.schemas.sensor_event import SensorEvent
from app.schemas.intent import Intent


class RoutingDecision(str, Enum):
    FAST_TRIGGER = "fast_trigger"
    MLLM_REASONER = "mllm_reasoner"
    THERAPIST_REMINDER = "therapist_reminder"
    CLINICAL_AGENT = "clinical_agent"
    DISCARD = "discard"


class AgentVerdict(str, Enum):
    EMERGENCY = "emergency"
    FALSE_POSITIVE = "false_positive"
    NEEDS_MONITORING = "needs_monitoring"
    PSYCHOLOGICAL = "psychological"
    CLINICAL = "clinical"


class AgentState(BaseModel):
    sensor_event: SensorEvent
    routing_decision: Optional[RoutingDecision] = None
    routing_confidence: Optional[float] = Field(
        default=None, ge=0.0, le=1.0
    )
    image_base64: Optional[str] = None
    audio_transcript: Optional[str] = None
    speech_wpm: Optional[float] = None
    verdict: Optional[AgentVerdict] = None
    verdict_confidence: Optional[float] = Field(
        default=None, ge=0.0, le=1.0
    )
    reasoning: Optional[str] = None
    guardrail_approved: bool = False
    guardrail_notes: Optional[str] = None
    final_intent: Optional[Intent] = None
    pipeline_start_time: datetime = Field(
        default_factory=datetime.now
    )
    error_message: Optional[str] = None

    class Config:
        use_enum_values = True