from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class IntentType(str, Enum):
    """
    Every possible action the robot can be asked to perform.
    The Pepper Interface Agent translates these into
    physical QiSDK calls on the Android app side.
    All 
    """
    # Movement
    NAVIGATE_TO = "navigate_to"          # go to a room
    RETURN_TO_BASE = "return_to_base"    # go back to charging station

    # Communication
    SPEAK = "speak"                      # say something to the patient
    SPEAK_AND_WAIT = "speak_and_wait"    # say something, wait for reply

    # Sensing (robot sends data back to backend)
    CAPTURE_IMAGE = "capture_image"      # take a photo and send it back
    CAPTURE_AUDIO = "capture_audio"      # record audio and send it back

    # Alerts
    ALERT_CAREGIVER = "alert_caregiver"  # notify nursing staff
    ALERT_EMERGENCY = "alert_emergency"  # call 112

    # Compound actions
    NAVIGATE_AND_SPEAK = "navigate_and_speak"  # go somewhere then speak
    WELLNESS_CHECK = "wellness_check"    # navigate + capture + speak


class UrgencyLevel(str, Enum):
    """
    How fast Pepper must act on this intent.
    LOW: routine reminder, no rush.
    MEDIUM: something needs checking soon.
    HIGH: potential emergency, act immediately.
    CRITICAL: confirmed emergency, override everything.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Intent(BaseModel):
    """
    A validated, guardrail-approved command sent to Pepper
    via WebSocket. Your colleague's Android app receives
    this JSON and translates it into physical robot actions.
    """

    # Tracing — links this command back to the original event
    event_id: str = Field(
        ...,
        description="The event_id from the SensorEvent that triggered this.",
        example="evt_20260509_001"
    )

    trace_id: str = Field(
        ...,
        description="Shared trace ID for the whole incident.",
        example="trace_fall_livingroom_001"
    )

    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When this intent was created by the backend."
    )

    # The command itself
    intent_type: IntentType = Field(
        ...,
        description="What the robot should do."
    )

    urgency: UrgencyLevel = Field(
        default=UrgencyLevel.MEDIUM,
        description="How urgently Pepper must act."
    )

    # Target location (required for navigation intents)
    target_location: Optional[str] = Field(
        default=None,
        description="Where Pepper should go. Required for NAVIGATE_TO.",
        example="living_room"
    )

    # Speech content (required for speak intents)
    speech_text: Optional[str] = Field(
        default=None,
        description=(
            "What Pepper should say. Required for SPEAK intents. "
            "Written in the patient's language. "
            "Max 200 characters to stay natural."
        ),
        max_length=200,
        example="Bonjour, c'est l'heure de vos médicaments !"
    )

    # Context for the robot's reasoning (not spoken aloud)
    context_note: Optional[str] = Field(
        default=None,
        description=(
            "Internal note for the robot about this situation. "
            "Not spoken. Used by the Android app to decide "
            "how to behave (gentle approach vs urgent)."
        ),
        example="Patient has not taken medication in 6 hours."
    )

    # Patient reference
    patient_id: Optional[str] = Field(
        default=None,
        description="Which patient this command concerns.",
        example="patient_001"
    )

    # Which agent produced this intent
    source_agent: str = Field(
        ...,
        description="Which agent created this intent. For logging.",
        example="therapist_reminder"
    )

    # Guardrail approval stamp
    guardrail_approved: bool = Field(
        default=False,
        description=(
            "Set to True by the Guardrail Agent after safety check. "
            "Intents with False are NEVER sent to the robot."
        )
    )

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "event_id": "evt_20260509_001",
                "trace_id": "trace_med_001",
                "intent_type": "navigate_and_speak",
                "urgency": "low",
                "target_location": "living_room",
                "speech_text": "Bonjour, c'est l'heure de vos médicaments !",
                "context_note": "Patient has not taken medication in 6 hours.",
                "patient_id": "patient_001",
                "source_agent": "therapist_reminder",
                "guardrail_approved": True
            }
        }