from __future__ import annotations

import re
import time
from typing import Any
from uuid import uuid4

from api.gengatewai.contracts import (
    DEV_LOOP,
    FRAMEWORK_SLUG,
    GATE_FIELDS,
    OPENAI_COMPATIBLE_RUNNER_MODEL,
)
from api.gengatewai.local_models import (
    LOCAL_MODEL_ID_PREFIX,
    LocalModelUnavailableError,
    call_local_chat_completion,
    discover_local_models,
    public_local_model,
    resolve_local_model,
)
from api.gengatewai.models import (
    GateEvaluationRequest,
    OpenAIChatCompletionChoice,
    OpenAIChatCompletionRequest,
    OpenAIChatCompletionResponse,
    OpenAIChatCompletionResponseMessage,
    OpenAIUsage,
)
from api.gengatewai.service import evaluate_gate, normalize_gate

MODEL_CREATED_AT = 1_788_048_000
RUNNER_SYSTEM_FINGERPRINT = "fp_doubt_the_machine_deterministic_v1"

GATE_LINE = re.compile(r"^\s*(CLAIM|FAILURE|EVIDENCE|TEST|REVERSAL)\s*[:=—-]\s*(.+?)\s*$", re.IGNORECASE)


class UnsupportedModelError(RuntimeError):
    """Raised when a requested OpenAI-compatible model id is not available."""


def openai_models() -> dict[str, Any]:
    try:
        local_models = [public_local_model(model) for model in discover_local_models()["models"]]
    except LocalModelUnavailableError:
        local_models = []

    return {
        "object": "list",
        "data": [
            {
                "id": OPENAI_COMPATIBLE_RUNNER_MODEL,
                "object": "model",
                "created": MODEL_CREATED_AT,
                "owned_by": "Dojo-1/doubt-the-machine",
            }
        ]
        + local_models,
    }


def openai_model(model_id: str) -> dict[str, Any] | None:
    for model in openai_models()["data"]:
        if model["id"] == model_id:
            return dict(model)
    return None


def message_content_to_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            for key in ("text", "input_text", "content"):
                value = item.get(key)
                if isinstance(value, str):
                    parts.append(value)
                    break
        return "\n".join(parts)
    return str(content)


def _messages_text(request: OpenAIChatCompletionRequest) -> list[tuple[str, str]]:
    return [(message.role, message_content_to_text(message.content).strip()) for message in request.messages]


def _metadata(request: OpenAIChatCompletionRequest) -> dict[str, Any]:
    return request.metadata or {}


def _metadata_string(metadata: dict[str, Any], key: str, default: str) -> str:
    value = metadata.get(key, default)
    return str(value).strip().lower() if value is not None else default


def _metadata_bool(metadata: dict[str, Any], key: str, default: bool = False) -> bool:
    value = metadata.get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def _gate_from_messages(texts: list[tuple[str, str]]) -> dict[str, str]:
    gate: dict[str, str] = {}
    for _, text in texts:
        for line in text.splitlines():
            match = GATE_LINE.match(line)
            if not match:
                continue
            field = match.group(1).upper()
            value = match.group(2).strip()
            if field in GATE_FIELDS and value and field not in gate:
                gate[field] = value
    return gate


def _gate_from_metadata(metadata: dict[str, Any]) -> dict[str, str]:
    raw_gate = metadata.get("gate") or metadata.get("doubt_gate") or {}
    if not isinstance(raw_gate, dict):
        return {}
    return normalize_gate({str(key): str(value) for key, value in raw_gate.items() if value is not None})


def _last_user_text(texts: list[tuple[str, str]]) -> str:
    for role, text in reversed(texts):
        if role == "user" and text:
            return text
    for _, text in reversed(texts):
        if text:
            return text
    return "No claim supplied."


def _gate_request_from_chat(request: OpenAIChatCompletionRequest) -> GateEvaluationRequest:
    texts = _messages_text(request)
    metadata = _metadata(request)
    gate = _gate_from_messages(texts)
    gate.update(_gate_from_metadata(metadata))
    claim = gate.get("CLAIM") or str(metadata.get("claim") or _last_user_text(texts)).strip()

    return GateEvaluationRequest(
        claim=claim,
        artifact="\n\n".join(text for _, text in texts if text) or None,
        artifact_origin=_metadata_string(metadata, "artifact_origin", "agent"),
        reviewer_type=_metadata_string(metadata, "reviewer_type", "agent"),
        uncertainty=_metadata_string(metadata, "uncertainty", "medium"),
        consequence=_metadata_string(metadata, "consequence", "medium"),
        reversibility=_metadata_string(metadata, "reversibility", "moderate"),
        external_claim=_metadata_bool(metadata, "external_claim"),
        experiment_or_metric=_metadata_bool(metadata, "experiment_or_metric"),
        active_rule_or_evidence_change=_metadata_bool(metadata, "active_rule_or_evidence_change"),
        gate=gate,
    )


def _format_list(values: list[str]) -> str:
    return ", ".join(values) if values else "none"


def _runner_message(request: OpenAIChatCompletionRequest) -> str:
    gate_request = _gate_request_from_chat(request)
    result = evaluate_gate(gate_request)
    gate = normalize_gate(gate_request.gate)

    lines = [
        "DOUBT → MEASURE → TEST → REVERT → REPEAT",
        "",
        f"Framework: {FRAMEWORK_SLUG}",
        f"Claim under review: {gate_request.claim}",
        f"Verification effort: {result.verification_effort}",
        f"Next required action: {result.next_required_action}",
        f"Missing gate fields: {_format_list(result.missing_gate_fields)}",
        "",
        "Gate record:",
    ]
    for field in GATE_FIELDS:
        lines.append(f"- {field}: {gate.get(field) or '[missing]'}")

    lines.extend(
        [
            "",
            "Reasons:",
            *(f"- {reason}" for reason in result.reasons),
            "",
            "Warnings:",
            *(f"- {warning}" for warning in result.warnings),
            "",
            "This OpenAI-compatible runner does not decide whether the claim is true, safe, or acceptable.",
        ]
    )
    return "\n".join(lines)


def _estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


def _json_fallback(value: dict[str, Any]) -> str:
    import json

    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _provider_content(provider_response: dict[str, Any]) -> str:
    choices = provider_response.get("choices", [])
    if isinstance(choices, list) and choices:
        choice = choices[0]
        if isinstance(choice, dict):
            message = choice.get("message", {})
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
            if isinstance(choice.get("text"), str):
                return choice["text"]
    return _json_fallback(provider_response)


def _provider_usage(provider_response: dict[str, Any], prompt_text: str, content: str) -> OpenAIUsage:
    raw_usage = provider_response.get("usage", {})
    if not isinstance(raw_usage, dict):
        raw_usage = {}
    prompt_tokens = int(raw_usage.get("prompt_tokens") or _estimate_tokens(prompt_text))
    completion_tokens = int(raw_usage.get("completion_tokens") or _estimate_tokens(content))
    total_tokens = int(raw_usage.get("total_tokens") or (prompt_tokens + completion_tokens))
    return OpenAIUsage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens)


def _local_runner_note() -> str:
    return (
        "GenGatewAI runner note: local model output above is advisory. "
        "It does not decide whether the claim is true, safe, or acceptable. "
        "Before belief, decision, execution, or persistence, complete CLAIM / FAILURE / EVIDENCE / TEST / REVERSAL."
    )


def _run_local_chat_completion(request: OpenAIChatCompletionRequest) -> OpenAIChatCompletionResponse:
    local_model = resolve_local_model(request.model)
    if local_model is None:
        raise UnsupportedModelError(f"unsupported model for this runner: {request.model}")

    request_payload = request.model_dump(mode="json", exclude_none=True)
    provider_response = call_local_chat_completion(request_payload, local_model)
    provider_content = _provider_content(provider_response)
    content = f"{provider_content}\n\n---\n{_local_runner_note()}"
    prompt_text = "\n".join(text for _, text in _messages_text(request))

    return OpenAIChatCompletionResponse(
        id=str(provider_response.get("id") or f"chatcmpl-dtm-local-{uuid4().hex}"),
        object="chat.completion",
        created=int(provider_response.get("created") or time.time()),
        model=request.model,
        choices=[
            OpenAIChatCompletionChoice(
                index=0,
                message=OpenAIChatCompletionResponseMessage(role="assistant", content=content),
                finish_reason="stop",
            )
        ],
        usage=_provider_usage(provider_response, prompt_text, content),
        system_fingerprint=f"{RUNNER_SYSTEM_FINGERPRINT}_local",
    )


def run_openai_chat_completion(request: OpenAIChatCompletionRequest) -> OpenAIChatCompletionResponse:
    if request.model.startswith(LOCAL_MODEL_ID_PREFIX):
        return _run_local_chat_completion(request)
    if request.model != OPENAI_COMPATIBLE_RUNNER_MODEL:
        raise UnsupportedModelError(f"unsupported model for this deterministic runner: {request.model}")

    content = _runner_message(request)
    prompt_text = "\n".join(text for _, text in _messages_text(request))
    prompt_tokens = _estimate_tokens(prompt_text)
    completion_tokens = _estimate_tokens(content)

    return OpenAIChatCompletionResponse(
        id=f"chatcmpl-dtm-{uuid4().hex}",
        object="chat.completion",
        created=int(time.time()),
        model=OPENAI_COMPATIBLE_RUNNER_MODEL,
        choices=[
            OpenAIChatCompletionChoice(
                index=0,
                message=OpenAIChatCompletionResponseMessage(role="assistant", content=content),
                finish_reason="stop",
            )
        ],
        usage=OpenAIUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
        system_fingerprint=RUNNER_SYSTEM_FINGERPRINT,
    )
