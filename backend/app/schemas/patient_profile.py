from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MobilityStatus(str, Enum):
    INDEPENDENT = "independent"
    WALKER = "walker"
    WHEELCHAIR = "wheelchair"
    BED_BOUND = "bed_bound"


class AlertThreshold(str, Enum):
    IMMEDIATE = "immediate"
    FIVE_MINUTES = "five_minutes"
    NURSE_ONLY = "nurse_only"
    FAMILY_FIRST = "family_first"


class Medication(BaseModel):
    name: str
    dose: str
    frequency: str
    last_taken: Optional[datetime] = None


class PatientProfile(BaseModel):
    patient_id: str
    full_name: str
    age: int = Field(..., ge=0, le=130)
    room_number: Optional[str] = None
    known_conditions: list[str] = []
    current_medications: list[Medication] = []
    known_allergies: list[str] = []
    baseline_speech_wpm: Optional[float] = None
    last_meal_timestamp: Optional[datetime] = None
    last_meal_description: Optional[str] = None
    mobility_status: MobilityStatus = MobilityStatus.INDEPENDENT
    fall_risk_score: Optional[float] = Field(
        default=None, ge=0.0, le=10.0
    )
    emergency_contact_name: str
    emergency_contact_phone: str
    caregiver_alert_threshold: AlertThreshold = (
        AlertThreshold.IMMEDIATE
    )
    preferred_language: str = "fr"
    clinical_notes: Optional[str] = None
    profile_last_updated: datetime = Field(
        default_factory=datetime.now
    )

    class Config:
        use_enum_values = True