# Универсальная платформа AI-возможностей

Универсальная платформа AI-возможностей — провайдер-нейтральный реестр, оценщик, роутер и runtime исполнения для разнородных AI-ресурсов: HF Spaces и Models, inference-провайдеров, REST/OpenAPI-сервисов, MCP-инструментов, A2A-агентов и внутренних API. Каноническая единица — **Capability + Contract**, а не iframe. Платформа обнаруживает возможности, проверяет машиночитаемые контракты, применяет политику, роутит в два этапа, исполняет долговечно и публикует вики для нейросетей.

🌐 **Язык / Language:** [Русский](README.ru.md) · [English](README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Deutsch](README.de.md)

## Ключевые факты

| Факт | Значение |
|------|----------|
| Каноническая единица | Capability + Contract |
| Ядро потока | Discovery → Registry → Contract → Evaluation → Policy → Routing → Execution → Composition → Deployment |
| Источник истины | PostgreSQL (SQLite для локальной разработки) |
| Knowledge graph | Производная проекция триплетов (`kg_entity` + `kg_triple`), ADR-002 |
| LLM-поверхность | `llms.txt`, `llms-full.txt`, 12 тематических страниц |
| Доменные сущности | 18 канонических таблиц |
| Таксономия ошибок | 15 нормализованных кодов |
| Проверка здоровья | `python scripts/health.py` (ruff + mypy + pytest) |
| Тесты | 56 проходят |
| Лицензия | MIT |

## Что отличает платформу

- **Tool ≠ Capability.** Tool — исполняемая реализация, Capability — устойчивая семантическая функция. Много инструментов могут удовлетворять одну возможность.
- **Resource ≠ Interface.** Model может открывать REST/SDK/MCP; Space — UI и Gradio API.
- **Двухэтапный роутинг.** Capability Router (семантика) никогда не сливается с Provider Router (рантайм-эндпоинт).
- **Найдено ≠ исполняемо.** Повышение доверия T0–T4 и полис-решение обязательны до внешнего вызова.
- **Контракты неизменяемы.** Исторические версии — append-only; дрейф создаёт новую версию и блокирует несовместимый роутинг.
- **Доказательства превыше всего.** Каждое утверждение помечено MEASURED / REPORTED (URL + дата) / INFERRED; неизвестное становится VERIFY, а не выдумкой.
- **Секреты не попадают в браузер.** Учётные данные провайдеров остаются на сервере, клиент получает scoped-токен.

## Быстрый старт

```bash
cd backend
python -m pip install -e ".[dev]"

# Идемпотентный сид: таблицы, граф, вики
$env:PYTHONPATH='src'   # Linux/macOS: export PYTHONPATH=src
python -m uaicp.seed

# Полная проверка
python scripts/health.py

# API
uvicorn uaicp.api.main:app --reload
```

Локальный PostgreSQL: `docker compose up -d db`, затем `DATABASE_URL` (см. `backend/.env.example`).

## Структура репозитория

```text
universal-ai-capability-platform-specs-v1/  исходный пакет спецификаций
.specify/                                    Spec Kit: конституция, шаблоны, скрипты
specs/001-knowledge-foundation/              вики + хранилище + knowledge graph
specs/002-contract-validation/               порты, совместимость, ошибки, CLI
specs/003-execution-gateway/                 автомат состояний, идемпотентность, повторы
backend/src/uaicp/                           код (domain, db, graph, wiki, api, validation, execution)
wiki/                                        сгенерированная база знаний для LLM
```

## Документация

- [Индекс базы знаний для LLM](wiki/llms.txt)
- [Полная база знаний](wiki/llms-full.txt)
- [Спецификация](universal-ai-capability-platform-specs-v1/universal-ai-capability-platform-specs-v1/docs/SPECS.md)
- [Конституция](.specify/memory/constitution.md)

## Методология

Проект построен по [GitHub Spec Kit](https://github.com/github/spec-kit): constitution → specify → plan → tasks → analyze → implement. У каждой фичи есть спецификация, план, задачи и тесты.

## Лицензия

MIT — см. [LICENSE](LICENSE).