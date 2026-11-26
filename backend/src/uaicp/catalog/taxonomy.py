"""Deterministic category taxonomy derived from HF Space tags (measured catalog data)."""

from __future__ import annotations

# Order matters: the first matching rule wins.
_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("image-generation", ("text-to-image", "image-generation", "image-gen", "stable-diffusion",
                          "flux", "text2image", "image generation")),
    ("image-editing", ("image-editing", "background-removal", "background removal",
                       "upscaler", "super-resolution", "image-to-image", "image editing",
                       "inpainting", "face-restoration")),
    ("video", ("image-to-video", "text-to-video", "video-generation", "video editing",
               "video", "animation")),
    ("audio-speech", ("text-to-speech", "tts", "voice-cloning", "voice cloning",
                      "transcription", "speech", "audio", "whisper", "music-generation",
                      "text-to-music")),
    ("ocr-document", ("ocr", "document-analysis", "document", "pdf", "layoutlm")),
    ("3d", ("3d", "3d-generation", "3d-model", "pose-estimation")),
    ("agents-mcp", ("mcp-server", "agents", "agent", "tool-use")),
    ("research-benchmarks", ("leaderboard", "benchmark", "research paper", "scientific paper",
                             "research-article-template", "evaluation", "ml-intern")),
    ("education", ("education", "tutorial", "course", "learning")),
    ("developer-tools", ("code-generation", "code", "data visualization", "fine-tuning",
                         "trl", "reinforcement-learning", "developer", "benchmarking")),
    ("text-nlp", ("text-generation", "text-classification", "summarization", "translation",
                  "question-answering", "chatbot", "llm", "text-analysis", "nlp")),
]


def categorize(tags: list[str] | None) -> str:
    lowered = {str(tag).lower() for tag in (tags or [])}
    for category, keywords in _RULES:
        if any(keyword in lowered for keyword in keywords):
            return category
    return "other"

CATEGORIES = [
    "image-generation", "image-editing", "video", "audio-speech", "ocr-document",
    "3d", "agents-mcp", "research-benchmarks", "education", "developer-tools",
    "text-nlp", "other",
]