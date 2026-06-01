from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class SensorType(str, Enum):
    MOTION = "motion"
    DOOR = "door"
    INACTIVITY = "inactivity"
    TEMPERATURE = "temperature"
    FALL_PROBABILITY = "fall_probability"
    MEDICATION_MISSED = "medication_missed"
    VOICE_DISTRESS = "voice_distress"


class Location(str, Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    BATHROOM = "bathroom"
    KITCHEN = "kitchen"
    HALLWAY = "hallway"
    UNKNOWN = "unknown"


class SensorEvent(BaseModel):
    event_id: str = Field(..., example="evt_001")
    trace_id: str = Field(..., example="trace_001")
    timestamp: datetime = Field(...)
    sensor_type: SensorType = Field(...)
    location: Location = Field(...)
    value: float = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    patient_id: Optional[str] = Field(default=None)
    metadata: Optional[dict] = Field(default=None)

    class Config:
        use_enum_values = True