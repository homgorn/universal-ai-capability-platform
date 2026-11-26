# Original research (source of truth)

**Source**: chat supplied by the owner, research dated 2026-10-07 (сообщено).
**Status**: reconstructed from the pasted message; the original chat file was not present on disk.
**Priority**: this document supersedes the spec package as the statement of intent.

## Core hypothesis

Build a universal AI tool registry, not an iframe catalog. A Space's iframe is only one field
of a Tool Descriptor. Canonical unit: capability + contract. Scale by composing tools, not by
mass-installing third-party iframes.

## Target chain

`HF/Replicate/fal/... → Ingestion → Normalization → Evaluation → Capability Graph → Planner → Recipes → Channel Adapters → Web/Telegram/Discord/Teams/LINE/...`

## Key decisions

1. **HF Hub/Spaces ≠ HF Inference Providers.** Spaces = app catalog + UI + API + MCP.
   Inference Providers = unified model routing (with `provider="auto"` failover). Do not mix.
2. **Four distinct operations**: Embed, API, Clone/duplicate, Rebuild. Embed ≠ right to copy code.
   Absence of a license is not permission to republish.
3. **Every Gradio Space is an API**: `/gradio_api/openapi.json`, `/gradio_api/call/<endpoint>` +
   `/gradio_api/call/<endpoint>/<event_id>`, and generated `agents.md`.
4. **MCP**: Spaces can be MCP servers; a Space is a capability provider, not an atomic tool.
5. **Capability graph** edges are output→input compatibility, using semantic type, MIME,
   dimensions, duration, language, quality and required metadata — not MIME alone.
6. **Hard gates before ranking**: license/legal, input compat, output compat, auth/security,
   channel compat, availability, policy/safety. Score is a heuristic only (0.30 task fit,
   0.20 quality, 0.15 reliability, 0.10 latency, 0.10 cost, 0.10 channel, 0.05 schema).
7. **Eight agent roles** named: Cataloger, Contract, Evaluator, Planner, Composer, Publisher,
   Monitor, License/Security Reviewer.
8. **Providers neutral from day one**; PostgreSQL is source of truth; graph edges relational on
   MVP; separate graph DB only when complexity is proven.
9. **Widget runtime own-hosted**: one stable widget host calls tools dynamically, instead of
   100k direct third-party iframes. SEO pages carry real indexable content; widget is part.
10. **Capability types**: MODEL, SPACE_APP, API_TOOL, MCP_TOOL, AGENT, RECIPE, ADAPTER,
    UI_WIDGET, CHANNEL_ADAPTER, DATASET, EVALUATOR.
11. **Deployment intent** is part of planning (channels, white_label, multi_tenant, seo,
    analytics) — the catalog becomes a deployment compiler.
12. **Tool → Capability → Recipe → App → Channel Deployment → Product/SaaS** hierarchy.

## MVP order (explicit in source)

- MVP-1 **HF Catalog Crawler**: Hub API → PostgreSQL → Tool Registry (id, author, title,
  category, tags, SDK, URL, likes, trending, runtime, last modified, SHA, license, models, datasets).
- MVP-2 Gradio Contract Extractor (agents.md + OpenAPI → canonical Tool Descriptor).
- MVP-3 Evaluator (schema valid, health, smoke test, latency, output validity).
- MVP-4 Widget Runtime (`widgets.example.com/t/{tool}`).
- MVP-5 Telegram Adapter.
- MVP-6 Planner.
- MVP-7 Provider abstraction (Replicate + fal).

Source says explicitly: do not start with million tools, Neo4j, own LLM, agent swarm,
auto-clone of every Space, own GPU infra or 20 channels.

## Research backlog from source

- R2-A full HF inventory: real volume, SDK/category distribution, Gradio/Docker/Static share,
  MCP-enabled, OpenAPI/agents.md presence, licenses, runtime availability.
- R2-B top-N quality benchmarks.
- R2-C competitor audit (Replicate, fal, Modal, Baseten, Together, RunPod, OpenRouter, MCP
  registries) — do not call a GitHub search match a competitor without audit.
- R2-D channel feasibility matrix.
- R2-E production specs 01…14 (architecture, registry, adapters, schemas, agents, evaluation,
  channels, widget, security, license, cost, observability, roadmap).

## Measured during our work (2026-11-26)

- `GET https://huggingface.co/api/spaces?limit=1&full=true` → 200, canonical fields present
  (`sha`, `cardData`, `tags`, `sdk`, `lastModified`, `subdomain`).
- Pagination: `Link: <...cursor=...>; rel="next"` header; no `x-total-count` header.
- `huggingface_hub` is installed locally; `HF_TOKEN` not set in env.

## RU

Источник: чат владельца 2026-10-07. Главный вывод — начинать с массового сбора HF Spaces и
Tool Registry, а не с архитектуры «сверху». iframe — лишь поле дескриптора. Порядок MVP:
crawler → contract extractor → evaluator → widget runtime → Telegram → planner → провайдеры.