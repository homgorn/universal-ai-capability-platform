"""Extract canonical ports from Gradio OpenAPI / agents.md (SPECS.md §5)."""

from __future__ import annotations

from uaicp.validation.fingerprint import canonical_fingerprint

_MIME_SEMANTIC = {
    "image/": "image",
    "audio/": "audio",
    "text/": "text",
    "video/": "video",
    "application/json": "json",
}


def semantic_from_mime(mime: str) -> str:
    for prefix, semantic in _MIME_SEMANTIC.items():
        if mime.startswith(prefix):
            return semantic
    return "binary"


def extract_from_openapi(schema: dict) -> dict:
    """Convert an OpenAPI schema into canonical input/output ports."""
    inputs: list[dict] = []
    outputs: list[dict] = []
    for path, methods in (schema.get("paths") or {}).items():
        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue
            name = path.strip("/").replace("/", "_") or method
            for mime, spec in (operation.get("requestBody") or {}).get("content", {}).items():
                inputs.append({
                    "name": name,
                    "required": True,
                    "semantic_type": semantic_from_mime(mime),
                    "transport_type": "HTTP_REST",
                    "schema": spec.get("schema") or {},
                })
            for code, response in (operation.get("responses") or {}).items():
                if not str(code).startswith("2"):
                    continue
                for mime, spec in (response.get("content") or {}).items():
                    outputs.append({
                        "name": name,
                        "required": True,
                        "semantic_type": semantic_from_mime(mime),
                        "transport_type": "HTTP_REST",
                        "schema": spec.get("schema") or {},
                    })
    return {
        "inputs": inputs,
        "outputs": outputs,
        "fingerprint": canonical_fingerprint(inputs, outputs),
    }


def extract_from_agents_md(text: str) -> dict:
    """Parse a minimal Gradio agents.md capability list."""
    capabilities = [
        line[2:].strip()
        for line in text.splitlines()
        if line.strip().startswith("- ")
    ]
    return {"capabilities": capabilities, "fingerprint": canonical_fingerprint(capabilities, [])}