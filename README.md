# Universal AI Capability Platform

The Universal AI Capability Platform is a provider-neutral registry built on top of Hugging Face Spaces: it crawls the public Space catalog, stores canonical records with raw snapshots, and will later derive capabilities, contracts, evaluations and plans from that measured inventory. The canonical unit is **Capability + Contract**; an embedded Space iframe is only one publication field, not the product. This repository currently implements **MVP-1 — the HF Catalog Crawler**, with the wiki, contract validation and execution gateway kept as reusable foundations.

🌐 **Language / Язык / 语言 / Idioma / Sprache:** [English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Deutsch](README.de.md)

## Facts at a glance

| Fact | Value |
|------|-------|
| Active feature | MVP-1 HF Catalog Crawler |
| Source | `https://huggingface.co/api/spaces` (Link cursor pagination) |
| Measured sample | 500 Spaces, 0 failures, 2026-11-26 |
| SDK split | gradio 334, static 98, docker 64, streamlit 5 |
| MCP-enabled | 89 Spaces carry `mcp-server` tag |
| License | 257 declared, 244 unknown |
| With models / datasets | 355 / 91 |
| Unique SHA | 492 of 501 records |
| Storage | PostgreSQL (SQLite locally), raw snapshots as JSON |
| Health | `python scripts/health.py` — ruff + mypy + pytest |
| License | MIT |

## Why the crawler is first

The original research (2026-10-07) started with a simple goal: extract all HF Spaces, then build
other layers on top. The earlier specification package described those upper layers first, which
produced a wiki and a site before a catalog existed. ADR-004 restores the order: **ingestion
before intelligence**. No planner, ranking, channel or SEO work is justified until the catalog is
measured.

## Roadmap (from the original research)

1. **HF Catalog Crawler** — active now: cursor pagination, checkpoints, SHA-based updates, dead letters.
2. **Gradio Contract Extractor** — `agents.md` + `/gradio_api/openapi.json` → canonical ports.
3. **Evaluator** — schema validity, health, smoke tests, latency, output validity.
4. **Widget Runtime** — one stable host calling tools dynamically, not 100k third-party iframes.
5. **Telegram Adapter** — bot commands + Mini App.
6. **Planner** — goal + deployment intent → recipe.
7. **Provider abstraction** — Replicate, fal and non-HF providers.

Do not build an own LLM, vector DB, graph DB, agent swarm, auto-clone of every Space or 20
channel adapters before the catalog exists.

## Quick start

```bash
cd backend
python -m pip install -e ".[dev]"

# Health first
python scripts/health.py

# Bounded live crawl (resumes from checkpoint)
set PYTHONPATH=src          # Windows PowerShell: $env:PYTHONPATH='src'
python -m uaicp.catalog.crawl --limit 500 --page-size 100

# Re-read a page with expanded fields
python -m uaicp.catalog.crawl --limit 500 --restart --refresh
```

No token is required for a bounded sample; `HF_TOKEN` raises rate limits for a full inventory.

## Repository layout

```text
docs/original-research-2026-10-07.md   source of intent (owner chat)
docs/adr/ADR-004-ingestion-first.md    reordering decision
specs/005-hf-catalog-crawler/          active SDD feature
backend/src/uaicp/catalog/             HF client, crawler, inventory report
backend/src/uaicp/{db,validation,execution,wiki,graph,ingestion}  foundations
wiki/                                  generated LLM-readable knowledge base
site/                                  Astro docs site (Cloudflare Workers)
```

## Method

Built with [GitHub Spec Kit](https://github.com/github/spec-kit): constitution → specify → plan → tasks → analyze → implement. Every feature has a spec, plan, tasks and tests.

## License

MIT — see [LICENSE](LICENSE).

---

RU: проект начинается с массового сбора HF Spaces; каноническая единица — Capability + Contract,
а iframe — лишь способ публикации. Сейчас активен MVP-1 сборщик каталога; вики, валидация
контрактов и execution-шлюз — фундамент для следующих слоёв. Полный инвентарь и лимиты API — VERIFY.