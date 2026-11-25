# Universal AI Capability Platform

The Universal AI Capability Platform is a provider-neutral registry, evaluator, router and execution runtime for heterogeneous AI resources — Hugging Face Spaces and Models, inference providers, REST/OpenAPI services, MCP tools, A2A agents and internal APIs. Its canonical unit is **Capability + Contract**, not an iframe. It discovers capabilities, verifies machine-readable contracts, enforces policy, routes in two stages, executes durably and publishes an LLM-readable wiki.

🌐 **Language / Язык / 语言 / Idioma / Sprache:** [English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Deutsch](README.de.md)

## Facts at a glance

| Fact | Value |
|------|-------|
| Canonical unit | Capability + Contract |
| Website | https://uacp-site.rvcdax.workers.dev |
| Core flow | Discovery → Registry → Contract → Evaluation → Policy → Routing → Execution → Composition → Deployment |
| Source of truth | PostgreSQL (SQLite for local dev) |
| Knowledge graph | Derived triple projection (`kg_entity` + `kg_triple`), ADR-002 |
| LLM surface | `llms.txt`, `llms-full.txt`, 12 topic pages |
| Domain entities | 18 canonical tables |
| Error taxonomy | 15 normalized codes |
| Health suite | `python scripts/health.py` (ruff + mypy + pytest) |
| Tests | 56 passing |
| License | MIT |

## What makes it different

- **Tool ≠ Capability.** A tool is an executable implementation; a capability is a stable semantic function. Many tools can satisfy one capability.
- **Resource ≠ Interface.** A Model may expose REST/SDK/MCP; a Space may expose UI and Gradio API.
- **Two-stage routing.** Capability Router (semantic fit) is never merged with Provider Router (runtime endpoint).
- **Discovered ≠ executable.** Trust promotion T0–T4 and a policy decision are mandatory before any external call.
- **Immutable contracts.** Historical contract versions are append-only; drift creates a new version and blocks incompatible routing.
- **Evidence first.** Every claim is marked MEASURED / REPORTED (URL + date) / INFERRED; unknowns become VERIFY items, never invented facts.
- **No secrets in the browser.** Provider credentials never reach clients; a scoped session token is used instead.

## Quick start

```bash
cd backend
python -m pip install -e ".[dev]"

# Idempotent seed: tables, graph, wiki
set PYTHONPATH=src          # Windows: $env:PYTHONPATH='src'
python -m uaicp.seed

# Verify everything
python scripts/health.py

# API
uvicorn uaicp.api.main:app --reload
```

PostgreSQL locally: `docker compose up -d db`, then set `DATABASE_URL` (see `backend/.env.example`).

## Repository layout

```text
universal-ai-capability-platform-specs-v1/  source specification package
.specify/                                    Spec Kit constitution, templates, scripts
specs/001-knowledge-foundation/              wiki + store + knowledge graph
specs/002-contract-validation/               ports, compatibility, error taxonomy, CLI
specs/003-execution-gateway/                 state machine, idempotency, retries, fallback
backend/src/uaicp/                           implementation (domain, db, graph, wiki, api, validation, execution)
wiki/                                        generated LLM-readable knowledge base
```

## Documentation

- [LLM knowledge base index](wiki/llms.txt)
- [Full knowledge base](wiki/llms-full.txt)
- [Specification](universal-ai-capability-platform-specs-v1/universal-ai-capability-platform-specs-v1/docs/SPECS.md)
- [Constitution](.specify/memory/constitution.md)

## Method

Built with [GitHub Spec Kit](https://github.com/github/spec-kit): constitution → specify → plan → tasks → analyze → implement. Every feature has a spec, plan, tasks and tests.

## License

MIT — see [LICENSE](LICENSE).