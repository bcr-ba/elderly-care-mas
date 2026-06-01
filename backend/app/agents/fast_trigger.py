from app.schemas.agent_state import AgentState, AgentVerdict
from app.schemas.intent import Intent, IntentType, UrgencyLevel

TEMPERATURE_HIGH = 38.0
TEMPERATURE_LOW = 15.0


def run_fast_trigger(state: AgentState) -> AgentState:
    event = state.sensor_event
    sensor = event.sensor_type
    value = event.value
    intent = None

    if sensor == "fall_probability" and value >= 0.90:
        intent = Intent(
            event_id=event.event_id,
            trace_id=event.trace_id,
            intent_type=IntentType.WELLNESS_CHECK,
            urgency=UrgencyLevel.CRITICAL,
            target_location=event.location,
            speech_text=(
                "Je suis là. "
                "Ne bougez pas, j'appelle les secours."
            ),
            context_note=(
                f"Fall probability {value:.0%}. "
                "Immediate response required."
            ),
            patient_id=event.patient_id,
            source_agent="fast_trigger",
            guardrail_approved=True
        )
        state.verdict = AgentVerdict.EMERGENCY
        print(f"[FAST_TRIGGER] CRITICAL fall → wellness_check")

    elif sensor == "temperature":
        if value >= TEMPERATURE_HIGH:
            speech = "Bonjour, avez-vous trop chaud ?"
            note = f"High temperature: {value}°C"
        else:
            speech = "Bonjour, avez-vous froid ?"
            note = f"Low temperature: {value}°C"
        intent = Intent(
            event_id=event.event_id,
            trace_id=event.trace_id,
            intent_type=IntentType.ALERT_CAREGIVER,
            urgency=UrgencyLevel.HIGH,
            target_location=event.location,
            speech_text=speech,
            context_note=note,
            patient_id=event.patient_id,
            source_agent="fast_trigger",
            guardrail_approved=True
        )
        state.verdict = AgentVerdict.EMERGENCY
        print(f"[FAST_TRIGGER] Temperature {value}°C → alert")

    else:
        intent = Intent(
            event_id=event.event_id,
            trace_id=event.trace_id,
            intent_type=IntentType.ALERT_CAREGIVER,
            urgency=UrgencyLevel.MEDIUM,
            context_note=f"Fast trigger: {sensor} = {value}",
            patient_id=event.patient_id,
            source_agent="fast_trigger",
            guardrail_approved=True
        )
        state.verdict = AgentVerdict.NEEDS_MONITORING
        print(f"[FAST_TRIGGER] Fallback → alert medium")

    state.final_intent = intent
    state.guardrail_approved = True
    return state