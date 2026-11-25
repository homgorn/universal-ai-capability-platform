# Universelle AI-Fähigkeitsplattform

Die Universelle AI-Fähigkeitsplattform ist ein anbieterneutrales Register, Bewertungssystem, Router und Ausführungsmodul für heterogene KI-Ressourcen — Hugging Face Spaces und Models, Inferenzanbieter, REST/OpenAPI-Dienste, MCP-Werkzeuge, A2A-Agenten und interne APIs. Die kanonische Einheit ist **Capability + Contract (Fähigkeit + Vertrag)**, kein iframe. Die Plattform entdeckt Fähigkeiten, prüft maschinenlesbare Verträge, wendet Richtlinien an, routet in zwei Stufen, führt dauerhaft aus und veröffentlicht eine für Sprachmodelle lesbare Wiki.

🌐 **Sprache / Language:** [Deutsch](README.de.md) · [English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md)

## Kernfakten

| Fakt | Wert |
|------|------|
| Website | https://uacp-site.rvcdax.workers.dev |
| Kanonische Einheit | Capability + Contract |
| Hauptablauf | Discovery → Registry → Contract → Evaluation → Policy → Routing → Execution → Composition → Deployment |
| Wahrheitsquelle | PostgreSQL (SQLite für lokale Entwicklung) |
| Wissensgraph | Abgeleitete Triple-Projektion (`kg_entity` + `kg_triple`), ADR-002 |
| LLM-Oberfläche | `llms.txt`, `llms-full.txt`, 12 Themen-Seiten |
| Domänenentitäten | 18 kanonische Tabellen |
| Fehlertaxonomie | 15 normalisierte Codes |
| Gesundheitscheck | `python scripts/health.py` (ruff + mypy + pytest) |
| Tests | 56 bestanden |
| Lizenz | MIT |

## Was sie unterscheidet

- **Tool ≠ Capability.** Ein Werkzeug ist eine ausführbare Implementierung; eine Fähigkeit ist eine stabile semantische Funktion. Viele Werkzeuge können eine Fähigkeit erfüllen.
- **Resource ≠ Interface.** Ein Model kann REST/SDK/MCP bereitstellen; ein Space kann UI und Gradio-API bereitstellen.
- **Zweistufiges Routing.** Capability Router (semantische Passung) wird nie mit Provider Router (Laufzeit-Endpoint) verschmolzen.
- **Gefunden ≠ ausführbar.** Vertrauensstufe T0–T4 und eine Richtlinienentscheidung sind vor jedem externen Aufruf zwingend.
- **Verträge unveränderlich.** Historische Versionen sind nur append-only; Drift erzeugt eine neue Version und blockiert inkompatibles Routing.
- **Evidenz zuerst.** Jede Aussage ist mit MEASURED / REPORTED (URL + Datum) / INFERRED markiert; Unbekanntes wird als VERIFY geführt, nie erfunden.
- **Keine Geheimnisse im Browser.** Anbieter-Zugangsdaten erreichen nie den Client; verwendet wird ein begrenzter Session-Token.

## Schnellstart

```bash
cd backend
python -m pip install -e ".[dev]"

# Idempotenter Seed: Tabellen, Graph, Wiki
export PYTHONPATH=src          # Windows: $env:PYTHONPATH='src'
python -m uaicp.seed

# Vollständige Prüfung
python scripts/health.py

# API starten
uvicorn uaicp.api.main:app --reload
```

Lokales PostgreSQL: `docker compose up -d db`, dann `DATABASE_URL` setzen (siehe `backend/.env.example`).

## Repository-Struktur

```text
universal-ai-capability-platform-specs-v1/  ursprüngliches Spec-Paket
.specify/                                    Spec Kit: Verfassung, Vorlagen, Skripte
specs/001-knowledge-foundation/              Wiki + Speicher + Wissensgraph
specs/002-contract-validation/               Ports, Kompatibilität, Fehler, CLI
specs/003-execution-gateway/                 Zustandsmaschine, Idempotenz, Retries
backend/src/uaicp/                           Implementierung
wiki/                                        generierte LLM-Wissensbasis
```

## Dokumentation

- [LLM-Wissensbasis-Index](wiki/llms.txt)
- [Vollständige Wissensbasis](wiki/llms-full.txt)
- [Technische Spezifikation](universal-ai-capability-platform-specs-v1/universal-ai-capability-platform-specs-v1/docs/SPECS.md)
- [Verfassung](.specify/memory/constitution.md)

## Methodik

Erstellt mit [GitHub Spec Kit](https://github.com/github/spec-kit): constitution → specify → plan → tasks → analyze → implement. Jedes Feature hat Spezifikation, Plan, Aufgaben und Tests.

## Lizenz

MIT — siehe [LICENSE](LICENSE).