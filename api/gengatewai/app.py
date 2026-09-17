from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.gengatewai.contracts import (
    API_VERSION,
    DEV_LOOP,
    OPENAI_COMPATIBLE_ENDPOINTS,
    OPENAI_COMPATIBLE_RUNNER_MODEL,
    SERVICE_NAME,
    experiment_summary,
    framework_contract,
)
from api.gengatewai.local_models import LocalModelUnavailableError, public_local_model_discovery
from api.gengatewai.models import (
    GateEvaluationRequest,
    GateEvaluationResponse,
    OpenAIChatCompletionRequest,
    OpenAIChatCompletionResponse,
    ReviewRecordsValidationRequest,
    ReviewRecordsValidationResponse,
)
from api.gengatewai.openai_compat import (
    UnsupportedModelError,
    openai_model,
    openai_models,
    run_openai_chat_completion,
)
from api.gengatewai.service import evaluate_gate, load_preregistration, validate_record_payloads

app = FastAPI(
    title="GenGatewAI",
    version=API_VERSION,
    summary="Deterministic API exposing the Doubt the Machine verification gate.",
)

# Mount static files for Vercel Web Analytics support
PUBLIC_DIR = Path(__file__).parent.parent.parent / "public"
if PUBLIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(PUBLIC_DIR)), name="static")


@app.get("/")
def service_index() -> dict[str, Any]:
    return {
        "service": SERVICE_NAME,
        "version": API_VERSION,
        "framework": "doubt-the-machine",
        "loop": " → ".join(DEV_LOOP),
        "openai_compatible_model": OPENAI_COMPATIBLE_RUNNER_MODEL,
        "endpoints": [
            "/healthz",
            "/web",
            *OPENAI_COMPATIBLE_ENDPOINTS,
            "/v1/gates/doubt-the-machine",
            "/v1/gates/doubt-the-machine/evaluate",
            "/v1/gates/doubt-the-machine/review-records/validate",
            "/v1/experiments/001-seeded-errors",
        ],
        "does_not_decide_truth": True,
    }


@app.get("/web")
def web_interface():
    """Serve the web interface with Vercel Web Analytics"""
    index_path = PUBLIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path), media_type="text/html")
    raise HTTPException(status_code=404, detail="Web interface not found")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"service": SERVICE_NAME, "version": API_VERSION, "status": "ok"}


@app.get("/v1/gates/doubt-the-machine")
def get_doubt_the_machine() -> dict[str, Any]:
    return framework_contract()


@app.get("/v1/models")
def list_openai_compatible_models() -> dict[str, Any]:
    return openai_models()


@app.get("/v1/local-models")
def list_local_model_capacity() -> dict[str, Any]:
    return public_local_model_discovery()


@app.get("/v1/models/{model_id:path}")
def get_openai_compatible_model(model_id: str) -> dict[str, Any]:
    model = openai_model(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail=f"model not found: {model_id}")
    return model


@app.post("/v1/chat/completions", response_model=OpenAIChatCompletionResponse)
def create_openai_compatible_chat_completion(
    request: OpenAIChatCompletionRequest,
) -> OpenAIChatCompletionResponse:
    if request.stream:
        raise HTTPException(
            status_code=400,
            detail="streaming is not supported by the deterministic Doubt runner yet",
        )
    try:
        return run_openai_chat_completion(request)
    except UnsupportedModelError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except LocalModelUnavailableError as exc:
        raise HTTPException(status_code=502, detail=f"local model unavailable: {exc}") from exc


@app.post("/v1/gates/doubt-the-machine/evaluate", response_model=GateEvaluationResponse)
def evaluate_doubt_gate(request: GateEvaluationRequest) -> GateEvaluationResponse:
    return evaluate_gate(request)


@app.post("/v1/gates/doubt-the-machine/review-records/validate", response_model=ReviewRecordsValidationResponse)
def validate_review_records(request: ReviewRecordsValidationRequest) -> ReviewRecordsValidationResponse:
    return validate_record_payloads(request)


@app.get("/v1/experiments/001-seeded-errors")
def get_experiment_001() -> dict[str, Any]:
    return experiment_summary(load_preregistration())
