<!--
Sync Impact Report
Version change: (none) → 1.0.0
Modified principles: none (initial ratification)
Added sections: Core Principles (7), Development Workflow, Quality Gates, Governance
Removed sections: none
Follow-up TODOs: none
-->

# Universal AI Capability Platform Constitution

## Core Principles

### I. Provider Neutrality
The core domain MUST remain provider-neutral. HF is the first source/adapter, never the
product boundary. Tool != Capability; Resource != Interface; Capability Router != Provider
Router. No provider-specific field may leak into the canonical domain without an ADR.

RU: Ядро домена остаётся провайдер-нейтральным. HF — первый источник/адаптер, а не
граница продукта. Tool ≠ Capability; Resource ≠ Interface; Capability Router ≠ Provider
Router. Провайдер-специфичные поля не попадают в канонический домен без ADR.

### II. Contracts Are Immutable and Versioned
Historical contracts MUST be immutable. Every normalized object carries provenance
(source, source_url, observed_at, source_revision, raw_snapshot, parser_version,
normalized_version). Schema fingerprints are deterministic; drift produces a new immutable
contract version and blocks incompatible routing.

RU: Исторические контракты неизменяемы. Каждый нормализованный объект несёт провенанс.
Детерминированный fingerprint схемы; дрейф создаёт новую неизменяемую версию контракта и
блокирует несовместимый роутинг.

### III. Discovered Is Not Executable
A discovered resource MUST NOT be executable by default. Trust promotion (T0–T4) and an
explicit policy decision (ALLOW | DENY | REQUIRE_APPROVAL | ALLOW_WITH_LIMITS) are required
before any external execution. Provider secrets MUST never reach browser clients.

RU: Найденный ресурс по умолчанию не исполним. Требуется повышение доверия (T0–T4) и
явное полис-решение. Секреты провайдеров никогда не попадают в браузер.

### IV. Evidence and Provenance First
Never invent provider prices, capabilities, limits, licenses or channel feasibility.
Every claim is marked as measured / reported (URL + date) / inferred. Unknowns become
explicit VERIFY gates, not fabricated facts. Public does not mean redistributable; license
state is explicit.

RU: Нельзя выдумывать цены, возможности, лимиты, лицензии и совместимость каналов.
Каждое утверждение помечается: измерено / сообщено (URL + дата) / выведено. Неизвестное
становится VERIFY-гейтом, а не вымыслом. Публичное ≠ разрешённое к распространению.

### V. Test-Backed Behavior
Every behavior has tests. Tests are written before or alongside implementation and must
fail first (Red-Green-Refactor). Acceptance criteria AT-01…AT-10 are release-blocking.
No production launch on model confidence or passing unit tests alone.

RU: У каждого поведения есть тесты. Тесты пишутся до/вместе с реализацией и сначала
падают. Критерии приёмки AT-01…AT-10 блокируют релиз. Запуск в прод не допускается на
основе уверенности модели или только unit-тестов.

### VI. Simplicity and YAGNI
PostgreSQL is the canonical source of truth. Do NOT build your own LLM, vector DB, graph DB,
browser engine, Kubernetes platform, billing processor or agent swarm. Integrate where
appropriate. Graph edges are relational until measured query complexity justifies a graph
database (ADR-002). A knowledge graph is a derived projection, not a new datastore, until
an ADR says otherwise.

RU: PostgreSQL — канонический источник истины. Не строим свой LLM, вектор-БД, граф-БД,
браузер, Kubernetes, биллинг или рой агентов. Граф — производная проекция (таблица
триплетов) до появления ADR на отдельную граф-БД.

### VII. LLM-Readable, Evidence-Dense Documentation
Documentation MUST be answer-first (direct fact in the first 150–300 characters under the
heading), fact-dense (exact numbers, tables, definition lists), and cite authoritative
first sources. Publish `llms.txt` and `llms-full.txt` alongside the human wiki. Russian and
English artifacts are both maintained (bilingual).

RU: Документация пишется answer-first (прямой факт в первых 150–300 символах),
факт-плотно (точные числа, таблицы, списки определений) и со ссылками на первоисточники.
Публикуются llms.txt и llms-full.txt. Артефакты ведутся двуязычно (RU + EN).

## Development Workflow

1. Read the relevant spec, schema and ADR before coding (AGENTS.md).
2. Work one bounded task at a time with explicit target files and acceptance criteria.
3. After coding run: formatter, linter, typecheck, unit tests, integration/contract tests.
4. Report: changed files, tests run, failures, assumptions, unresolved VERIFY/TODO,
   security impact, migration impact.
5. Architectural changes require an ADR; do not redesign during implementation.
6. Never delete user data or files without double confirmation.

RU: Перед кодом читаем spec/schema/ADR. Работаем одной ограниченной задачей. После —
форматтер, линтер, typecheck, unit/integration/contract тесты и отчёт по чек-листу.
Архитектурные изменения — только через ADR. Ничего не удаляем без двойного подтверждения.

## Quality Gates

- Constitution Check gate before Phase 0 and after Phase 1 design.
- Spec quality checklist before planning.
- Cross-artifact analyze before implement.
- Security/trust/policy review for every external execution path.
- Production gates (SPECS.md §22) before any launch.

RU: Constitution Check до Phase 0 и после Phase 1. Чек-лист качества спеки до плана.
Analyze перед реализацией. Security/trust/policy-ревью каждого внешнего исполнения.
Production gates (§22) до любого запуска.

## Governance

This constitution supersedes other practices. Amendments require a documented change,
version bump (MAJOR/MINOR/PATCH), and migration plan. All specs, plans and tasks MUST
verify compliance. Complexity must be justified in the plan's Complexity Tracking table.
Runtime development guidance lives in AGENTS.md and the spec package.

**Version**: 1.0.0 | **Ratified**: 2026-11-25 | **Last Amended**: 2026-11-25