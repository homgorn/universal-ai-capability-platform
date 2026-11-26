"""Convert /gradio_api/info parameters into canonical ports."""

from __future__ import annotations

_SEMANTIC = (
    ("image", "image"),
    ("audio", "audio"),
    ("video", "video"),
    ("file", "binary"),
    ("number", "number"),
    ("integer", "number"),
    ("boolean", "boolean"),
    ("string", "text"),
)


def semantic_type(type_hint: str | None) -> str:
    hint = (type_hint or "").lower()
    for needle, semantic in _SEMANTIC:
        if needle in hint:
            return semantic
    return "text"


def _param_name(param: dict) -> str:
    return str(param.get("parameter_name") or param.get("name") or "input")


def ports_from_info(info: dict) -> dict:
    """Return canonical inputs/outputs from a Gradio /gradio_api/info payload."""
    inputs: list[dict] = []
    outputs: list[dict] = []
    endpoints = info.get("named_endpoints") or {}
    if not isinstance(endpoints, dict):
        return {"inputs": inputs, "outputs": outputs}
    for name, spec in endpoints.items():
        if not isinstance(spec, dict):
            continue
        parameters = spec.get("parameters") or []
        for param in parameters:
            if not isinstance(param, dict):
                continue
            hint = str(param.get("type") or param.get("python_type") or "string")
            inputs.append({
                "name": _param_name(param),
                "required": bool(param.get("required", True)),
                "semantic_type": semantic_type(hint),
                "transport_type": "GRADIO",
                "schema": {"type": hint},
                "constraints": param.get("constraints") or {},
                "examples": param.get("examples") or [],
                "sensitive": False,
                "artifact_type": "file" if "file" in hint.lower() else None,
            })
        outputs.append({
            "name": f"{name}_result",
            "required": True,
            "semantic_type": "binary",
            "transport_type": "GRADIO",
            "schema": {"type": "output"},
        })
    return {"inputs": inputs, "outputs": outputs}