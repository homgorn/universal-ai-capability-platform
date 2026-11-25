# Feature Specification: Knowledge Foundation

**Feature Branch**: `001-knowledge-foundation`

**Created**: 2026-11-25

**Status**: Draft

**Input**: User description: "Knowledge Foundation: LLM-readable wiki (llms.txt + llms-full.txt + markdown), canonical persistent store, and a derived knowledge graph of entities and triples for the Universal AI Capability Platform."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read the platform through an LLM-readable wiki (Priority: P1)

A human reader or an AI search/answer engine (Perplexity, ChatGPT Search, Google AI
Overviews, Gemini, Claude) can retrieve a compact, answer-first, fact-dense description of
the platform, its core entities, contracts and invariants, and cite it without
hallucination.

**Why this priority**: Without an authoritative, machine-readable knowledge surface the
platform cannot be discovered, cited or trusted by AI clients; this is the entry point for
every other capability.

**Independent Test**: Fetch the published `llms.txt`; verify it lists the platform, its
entities and contracts with links; verify the first content chunk under the top heading
answers "what this platform is" in 40–80 words with exact facts.

**Acceptance Scenarios**:

1. **Given** a consumer requests the knowledge surface, **When** it reads the first chunk,
   **Then** it gets a direct factual answer (name, purpose, canonical unit, core flow).
2. **Given** a consumer follows a link to a topic page, **When** it reads that page, **Then**
   the answer-first paragraph appears within the first 150–300 characters.
3. **Given** an AI engine parses the wiki, **When** it extracts tables and definition
   lists, **Then** it obtains exact numbers and definitions rather than marketing prose.

---

### User Story 2 - Persist the canonical domain (Priority: P1)

The platform can durably store every canonical domain entity with tenant isolation,
immutable historical contracts and full provenance, so that discovery, evaluation and
execution all read from one source of truth.

**Why this priority**: A registry without durable, isolated, provenance-carrying storage is
a throwaway catalog; all routing, evaluation and audit depend on it.

**Independent Test**: Write and read back each entity; confirm tenant A cannot read tenant
B's rows; confirm a contract version, once written, cannot be mutated; confirm every row
carries provenance fields.

**Acceptance Scenarios**:

1. **Given** a normalized object with provenance, **When** it is stored, **Then** all
   provenance fields persist and are retrievable.
2. **Given** tenant A and tenant B, **When** A queries, **Then** B's executions, artifacts
   and credentials are never returned.
3. **Given** an immutable contract version, **When** a schema change arrives, **Then** a new
   version is created and the old one is unchanged.

---

### User Story 3 - Query a knowledge graph of entities and triples (Priority: P2)

A consumer can query relationships between entities as `(subject, predicate, object)`
triples — for example which tools implement a capability, which provider owns a resource,
which contracts an execution used — and traverse them.

**Why this priority**: Relationships are first-class product data (Tool→Capability,
Resource→Interface, Capability→Contract); a triple projection makes them queryable without
committing to a graph database.

**Independent Test**: Ingest entities, generate triples, query by entity and by triple
pattern, and verify the expected relationships are returned.

**Acceptance Scenarios**:

1. **Given** stored entities, **When** triples are generated, **Then** each expected
   relationship exists as a triple with source entity and mark.
2. **Given** a triple pattern query, **When** it runs, **Then** matching triples return in
   bounded time with tenant filtering.
3. **Given** the graph is a derived projection, **When** the source store changes, **Then**
   the graph can be rebuilt deterministically.

---

### User Story 4 - Mark evidence and surface unknowns (Priority: P2)

Every stored claim carries an evidence mark — measured / reported (with URL and date) /
inferred — and any value that cannot be verified is flagged as a VERIFY gate instead of
being invented.

**Why this priority**: The platform's value is trustworthy capability intelligence;
fabricated prices, limits or licenses would poison every downstream decision.

**Independent Test**: Attempt to store a claim with no provenance; verify rejection.
Store a reported claim with URL+date; verify it is accepted and marked.

**Acceptance Scenarios**:

1. **Given** a claim without provenance, **When** stored, **Then** it is rejected.
2. **Given** a reported claim, **When** stored, **Then** source URL and observed date are
   mandatory and persisted.
3. **Given** an unknown value, **When** the wiki is generated, **Then** it appears as a
   VERIFY item, not as a fact.

---

### User Story 5 - Regenerate the wiki deterministically (Priority: P3)

A maintainer can regenerate `llms.txt`, `llms-full.txt` and the markdown wiki from the
store and specs, and the output is stable for unchanged inputs.

**Why this priority**: The wiki must stay in sync with the source of truth without manual
drift; automation is the polish that keeps it trustworthy.

**Independent Test**: Run the generator twice on unchanged inputs; diff the outputs; expect
no differences.

**Acceptance Scenarios**:

1. **Given** unchanged inputs, **When** the generator runs twice, **Then** outputs are
   byte-identical.
2. **Given** a changed entity, **When** regenerated, **Then** only the affected pages
   change.

---

### Edge Cases

- A resource with no declared compatible data class MUST NOT receive confidential or
  restricted data.
- A discovered resource MUST NOT become executable without trust promotion and policy.
- A schema fingerprint change with unknown compatibility MUST block routing.
- A triple referencing a deleted/unknown entity MUST be handled without orphaning the graph.
- Very large artifacts MUST be referenced, not embedded in the knowledge surface (out of scope
  for this feature; artifacts are referenced by URI only).
- Empty wiki inputs MUST still produce a valid, non-misleading `llms.txt`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The platform MUST publish an LLM-readable knowledge surface consisting of
  `llms.txt`, `llms-full.txt` and a markdown wiki.
- **FR-002**: The knowledge surface MUST be answer-first: a direct factual answer within the
  first 150–300 characters under each top heading.
- **FR-003**: The platform MUST persist all canonical domain entities with tenant isolation.
- **FR-004**: Historical contracts MUST be immutable; changes MUST create new versions.
- **FR-005**: Every stored object MUST carry provenance (source, source_url, observed_at,
  source_revision, raw_snapshot, parser_version, normalized_version).
- **FR-006**: The platform MUST expose a knowledge graph of `(subject, predicate, object)`
  triples derived from stored entities.
- **FR-007**: The graph MUST be queryable by entity and by triple pattern, with tenant
  filtering.
- **FR-008**: Every claim MUST carry an evidence mark — measured / reported (URL + date) /
  inferred — in addition to the provenance required by FR-005.
- **FR-009**: Unverifiable values MUST be flagged as VERIFY gates, never fabricated.
- **FR-010**: The wiki MUST be regenerable deterministically from the store and specs.
- **FR-011**: The system MUST enforce that discovered != executable (a Capability's default
  status is DISCOVERED and it MUST NOT be ACTIVE without explicit promotion) and that provider
  secrets never reach browser clients. This is an enforced, test-verified invariant, not a
  documentation-only statement.
- **FR-012**: The system MUST record a machine-readable index of entities and triples (JSON,
  per `contracts/graph-query.md`).

### Key Entities *(include if feature involves data)*

- **Provider**: organization/system exposing resources or execution.
- **Resource**: provider-owned/discovered thing (MODEL, SPACE, API_SERVICE, MCP_SERVER,
  AGENT_SERVICE, DATASET, REPOSITORY).
- **Interface**: access mechanism (HTTP_REST, OPENAPI, GRADIO, MCP, A2A, SDK, EMBED,
  WEBHOOK, CLI).
- **Operation**: callable action (e.g. generate, transcribe, remove_background).
- **Tool**: executable implementation of an operation (references Resource + Interface +
  Operation).
- **Capability**: stable semantic function (e.g. image.background_remove).
- **Contract**: machine-readable input/output constraints, immutable and versioned.
- **Evaluation**: evidence about correctness, quality, latency, reliability, safety, cost.
- **Health**: availability, p50/p95 latency, error rate, queue delay, quota, schema status.
- **Policy**: decision (ALLOW | DENY | REQUIRE_APPROVAL | ALLOW_WITH_LIMITS) and version.
- **Provenance**: source and revision metadata attached to every normalized object.
- **Execution**: durable logical runtime operation with attempts, events and cost.
- **Artifact**: typed input/output persisted outside model context.
- **Recipe**: provider-neutral composition of capabilities/operations (typed DAG).
- **App**: user-facing application built from recipes.
- **Deployment**: publication of an App/Recipe to a channel and tenant.
- **Entity (graph)**: a node in the knowledge graph referencing a domain entity.
- **Triple (graph)**: `(subject, predicate, object)` edge with provenance and mark.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An AI answer engine can state the platform's purpose and canonical unit from
  the first chunk of `llms.txt`; 0 fabricated facts and 100% of claims carry an evidence mark.
- **SC-002**: 100% of stored domain rows carry complete provenance; 0 rows without it.
- **SC-003**: Tenant isolation holds for 100% of cross-tenant access attempts (0 leaks).
- **SC-004**: A contract version, once written, has 0 mutations across a drift test.
- **SC-005**: Triple queries by entity and pattern return correct results for a seeded
  fixture set with 100% precision and return in under 100 ms on that fixture.
- **SC-006**: Regenerating the wiki on unchanged inputs yields byte-identical output.
- **SC-007**: 100% of unverifiable values appear as VERIFY items; 0 fabricated facts.

## Assumptions

- The source specification package (`docs/SPECS.md`, contracts, schemas, ADRs) is the
  authoritative basis and is treated as read-only reference.
- The knowledge graph is a derived projection over the canonical store, not a separate
  datastore, until an ADR approves a graph database.
- Bilingual (EN + RU) artifacts are maintained; English is canonical for technical terms.
- No production launch occurs in this feature; production gates are out of scope here.
- Provider prices, limits and licenses are unknown and MUST remain VERIFY items.

---

## RU — Резюме спецификации

**Фича**: Knowledge Foundation — фундамент знаний платформы.

**Пользовательские истории**:
- US1 (P1): LLM-вики (`llms.txt`, `llms-full.txt`, markdown) — answer-first, факт-плотно,
  цитируемо нейросетями.
- US2 (P1): каноническое хранилище всех сущностей с изоляцией тенантов, неизменяемыми
  контрактами и провенансом.
- US3 (P2): knowledge graph из триплетов `(subject, predicate, object)` как производная
  проекция, с запросом по сущности и по паттерну.
- US4 (P2): маркировка доказательств (измерено / сообщено URL+дата / выведено) и VERIFY для
  неизвестного.
- US5 (P3): детерминированная регенерация вики из хранилища и спек.

**Ключевые требования**: FR-001…FR-012 (вики, answer-first, провенанс, неизменяемость,
триплеты, tenant isolation, evidence marks, VERIFY, детерминизм).

**Критерии успеха**: SC-001…SC-007 (цитируемость, 100% провенанс, 0 утечек между тенантами,
0 мутаций контрактов, точность триплетов, байт-идентичная регенерация, 0 выдуманных фактов).

**Допущения**: спеки — read-only база; граф — проекция, не отдельная БД (до ADR); двуязычность;
без production-запуска; цены/лимиты/лицензии — только VERIFY.