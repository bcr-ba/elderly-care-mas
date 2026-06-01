from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.schemas.sensor_event import SensorEvent
from app.schemas.agent_state import AgentState


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("MAS Backend starting...")
    from app.core.graph import pipeline
    app.state.pipeline = pipeline
    print("LangGraph pipeline ready")
    yield
    print("MAS Backend shutting down...")


app = FastAPI(
    title="Multi-Agent System - Elderly Care",
    description="Backend decision engine for elderly care robots",
    version="0.2.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {
        "status": "running",
        "version": "0.2.0",
        "built": ["classifier", "fast_trigger"],
        "pending": ["mllm_reasoner", "guardrail",
                    "therapist", "clinical"]
    }


@app.get("/health")
async def health():
    return {
        "backend": "ok",
        "pipeline": "loaded",
        "mqtt": "not connected yet",
        "ollama": "not connected yet"
    }


@app.post("/api/v1/events")
async def receive_event(event: SensorEvent):
    from app.core.graph import pipeline
    state = AgentState(sensor_event=event)
    print(f"\n{'='*50}")
    print(f"EVENT: {event.event_id} | "
          f"{event.sensor_type} | {event.value}")
    print(f"{'='*50}")
    result = await pipeline.ainvoke(state)
    response = {
        "event_id": event.event_id,
        "routing_decision": result.get("routing_decision"),
        "guardrail_approved": result.get("guardrail_approved"),
        "verdict": result.get("verdict"),
    }
    final = result.get("final_intent")
    if final:
        if hasattr(final, 'model_dump'):
            response["intent"] = final.model_dump()
        else:
            response["intent"] = final
    return response