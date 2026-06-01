from app.schemas.agent_state import AgentState, RoutingDecision

FALL_EMERGENCY_THRESHOLD = 0.90
FALL_CONFIDENCE_THRESHOLD = 0.85
INACTIVITY_MLLM_SECONDS = 1800
VOICE_DISTRESS_THRESHOLD = 0.70
TEMPERATURE_HIGH = 38.0
TEMPERATURE_LOW = 15.0


def run_classifier(state: AgentState) -> AgentState:
    event = state.sensor_event
    sensor = event.sensor_type
    value = event.value
    confidence = event.confidence

    if sensor == "fall_probability":
        if (value >= FALL_EMERGENCY_THRESHOLD and
                confidence >= FALL_CONFIDENCE_THRESHOLD):
            state.routing_decision = RoutingDecision.FAST_TRIGGER
            state.routing_confidence = confidence
            print(f"[CLASSIFIER] fall {value:.2f} → FAST_TRIGGER")
        else:
            state.routing_decision = RoutingDecision.MLLM_REASONER
            state.routing_confidence = confidence
            print(f"[CLASSIFIER] fall {value:.2f} ambiguous → MLLM")
        return state

    if sensor == "inactivity":
        if value >= INACTIVITY_MLLM_SECONDS:
            state.routing_decision = RoutingDecision.MLLM_REASONER
            state.routing_confidence = 0.80
            print(f"[CLASSIFIER] inactivity {value:.0f}s → MLLM")
        else:
            state.routing_decision = RoutingDecision.DISCARD
            state.routing_confidence = 1.0
            print(f"[CLASSIFIER] inactivity {value:.0f}s short → DISCARD")
        return state

    if sensor == "medication_missed":
        state.routing_decision = RoutingDecision.THERAPIST_REMINDER
        state.routing_confidence = 0.95
        print(f"[CLASSIFIER] medication_missed → THERAPIST")
        return state

    if sensor == "voice_distress":
        if confidence >= VOICE_DISTRESS_THRESHOLD:
            state.routing_decision = RoutingDecision.MLLM_REASONER
            state.routing_confidence = confidence
            print(f"[CLASSIFIER] voice_distress → MLLM")
            return state

    if sensor == "temperature":
        if value >= TEMPERATURE_HIGH or value <= TEMPERATURE_LOW:
            state.routing_decision = RoutingDecision.FAST_TRIGGER
            state.routing_confidence = 0.99
            print(f"[CLASSIFIER] temp {value}°C → FAST_TRIGGER")
            return state

    state.routing_decision = RoutingDecision.DISCARD
    state.routing_confidence = 1.0
    print(f"[CLASSIFIER] {sensor} → DISCARD")
    return state