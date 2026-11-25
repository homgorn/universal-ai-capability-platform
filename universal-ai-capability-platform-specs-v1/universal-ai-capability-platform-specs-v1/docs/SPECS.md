# Universal AI Capability Platform — Implementation Specs v1.0

Status: IMPLEMENTATION DRAFT / VERIFY BEFORE PRODUCTION

## 0. Mission

Build a provider-neutral capability intelligence and execution layer over heterogeneous AI resources: HF Spaces/Models, inference providers, REST/OpenAPI services, MCP tools, A2A agents and internal services.

Canonical unit: **Capability + Contract**, not iframe.

Core flow:

`Discovery → Registry → Contract → Evaluation → Policy → Routing → Execution → Composition → Deployment`

Product chain:

`Tool → Capability → Recipe → App → Channel Deployment → Product`

## 1. Architecture after self-critique

### Correction 1: HF is not the product boundary
HF is the first source/adapter. Core domain MUST remain provider-neutral.

### Correction 2: never overload Tool Descriptor
Separate entities:
- Provider
- Resource
- Interface
- Operation
- Tool
- Capability
- Contract
- Evaluation
- Health
- Policy
- Provenance
- Execution
- Artifact
- Recipe
- App
- Deployment

### Correction 3: Tool != Capability
Tool = executable implementation.
Capability = normalized semantic function.
Multiple tools can implement one capability.

### Correction 4: Model/Space/API are not the same thing
Resource type and interface type are independent. A Model may expose REST/SDK/MCP; a Space may expose UI and Gradio API; an external service may expose OpenAPI without being a model.

### Correction 5: no graph DB initially
PostgreSQL is source of truth. Graph edges are relational until measured query complexity proves the need for a graph database.

### Correction 6: planner comes after contracts/evaluation/policy
Do not start with autonomous agent swarm. First make deterministic safe execution work.

### Correction 7: quality is multidimensional
Do not rely on one weighted score. Store quality, reliability, latency, cost and safety independently; use policy-specific ranking profiles.

### Correction 8: public does not mean redistributable
License state must be explicit. Unknown/restricted licenses cannot automatically enter white-label production.

### Correction 9: health is not boolean
Track availability, p50/p95 latency, error rate, queue delay, quota and schema drift over time.

### Correction 10: economics is runtime policy
Estimate cost before execution, capture actual cost, enforce budgets and record margin separately.

### Correction 11: execution is a first-class durable entity
A registry without execution semantics is a catalog. Execution requires idempotency, cancellation, retry policy, fallback attempts, events and artifacts.

### Correction 12: channel feasibility must be tested
Web/Telegram/Discord/Teams/LINE/bot channels have different constraints. Every adapter needs a capability/constraint contract and tests.

## 2. Domain model

### Provider
Organization/system exposing resources or execution.

### Resource
Provider-owned/discovered thing.
Types: `MODEL`, `SPACE`, `API_SERVICE`, `MCP_SERVER`, `AGENT_SERVICE`, `DATASET`, `REPOSITORY`.

### Interface
Access mechanism.
Types: `HTTP_REST`, `OPENAPI`, `GRADIO`, `MCP`, `A2A`, `SDK`, `EMBED`, `WEBHOOK`, `CLI`.

### Operation
Callable action, e.g. `generate`, `transcribe`, `remove_background`.

### Tool
Executable implementation of an operation. References Resource + Interface + Operation.

### Capability
Stable semantic function, e.g. `image.background_remove`.

### Contract
Machine-readable input/output constraints.

### Evaluation
Evidence about contract correctness, quality, latency, reliability, safety and cost.

### Recipe
Provider-neutral composition of capabilities/operations.

### Execution
One logical runtime operation or recipe run, containing one or more attempts.

### Artifact
Typed input/output persisted outside model context.

### Deployment
Publication of an App/Recipe to a channel and tenant.

## 3. Capability registry

Capability ID format: `<domain>.<function>`.
Examples:
- `image.background_remove`
- `image.upscale`
- `video.image_to_video`
- `audio.transcribe`
- `document.extract_text`

Lifecycle:
`DRAFT → DISCOVERED → CONTRACT_VERIFIED → EVALUATED → APPROVED → ACTIVE → DEGRADED → SUSPENDED → DEPRECATED`

A discovered resource MUST NOT be executable by default.

Search modes:
1. exact
2. keyword
3. semantic intent
4. contract compatibility
5. hybrid quality/cost/latency search

## 4. Contract architecture

Never discard provider-native schemas. Store them as immutable provenance snapshots.

Canonical input port:
- name
- required
- semantic_type
- transport_type
- schema
- constraints
- examples
- sensitive
- artifact_type

Canonical output port has the same structure plus persistence metadata.

Compatibility is NOT only MIME matching. Check:
- transport
- semantic type
- schema
- cardinality
- required metadata
- dimensions/duration
- language
- size limits

### Error taxonomy
`INVALID_INPUT`, `CONTRACT_MISMATCH`, `AUTH_REQUIRED`, `AUTH_FAILED`, `POLICY_DENIED`, `RATE_LIMITED`, `QUOTA_EXCEEDED`, `PROVIDER_UNAVAILABLE`, `PROVIDER_TIMEOUT`, `SCHEMA_DRIFT`, `ARTIFACT_TOO_LARGE`, `ARTIFACT_UNSAFE`, `EXECUTION_CANCELLED`, `EXECUTION_FAILED`, `INTERNAL_ERROR`.

Every normalized error MUST include `code`, `message`, `retryable`, `stage`, `details`; optionally `retry_after` and provider error.

## 5. Discovery and ingestion

Initial adapters:
1. HF Spaces
2. HF Models / Inference Providers
3. generic OpenAPI/REST
4. MCP
5. Replicate
6. fal
7. internal APIs

Discovery pipeline:

`source → raw snapshot → normalization → contract extraction → fingerprint → policy/evaluation queue`

HF-specific implementation should attempt:
- Hub listing/search
- raw resource metadata
- revision/SHA
- Gradio `agents.md`
- Gradio OpenAPI schema
- MCP metadata where applicable

Crawler requirements:
- pagination
- bounded concurrency
- exponential backoff + jitter
- 429 handling
- caching
- change detection
- dead-letter queue
- resumability

Discovery MUST NOT execute arbitrary provider code merely because a resource was found.

## 6. Trust and security

Trust tiers:
- `T0`: metadata only
- `T1`: schema inspection
- `T2`: sandboxed smoke test
- `T3`: controlled production execution
- `T4`: privileged/private connector

Threats:
SSRF, malicious files, arbitrary code, prompt injection, secret exfiltration, data leakage, runaway cost, malicious MCP tools, compromised dependencies, cross-tenant access.

Required controls:
- outbound allowlist
- SSRF protection
- private network blocking unless explicitly approved
- secret isolation
- short-lived credentials
- tenant isolation
- file size/type limits
- malware scanning decision
- audit log
- rate limits
- budget limits
- human approval for privileged operations

Policy decision:
`ALLOW | DENY | REQUIRE_APPROVAL | ALLOW_WITH_LIMITS`

Data classification:
`PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED`.

A tool that does not declare compatible data classes MUST NOT receive confidential/restricted data.

## 7. Provenance and drift

Every normalized object stores:
- source
- source_url
- observed_at
- source_revision
- raw_snapshot
- parser_version
- normalized_version

Compute deterministic schema fingerprint.

On fingerprint change:
1. create drift event
2. preserve old contract
3. extract new contract
4. compare
5. classify compatibility
6. re-evaluate
7. block routing if incompatible/unknown under policy

Compatibility:
`PATCH_COMPATIBLE | BACKWARD_COMPATIBLE | BREAKING | UNKNOWN`.

Historical contracts MUST be immutable.

## 8. Routing

### Stage A — Capability Router
Selects implementations satisfying the semantic goal and contract.

### Stage B — Provider Router
Selects the concrete provider/endpoint at runtime.

Never merge these stages.

Hard gates before scoring:
1. policy/legal
2. input/output compatibility
3. security/trust
4. auth
5. channel constraints
6. availability
7. budget

Ranking dimensions:
- task fit
- empirical quality
- reliability
- latency
- cost efficiency
- schema quality
- tenant preference

Profiles:
`QUALITY_FIRST`, `BALANCED`, `CHEAPEST_VALID`, `LOW_LATENCY`, `PRIVATE`, `SELF_HOSTED`.

Every routing decision records candidate set, rejection reasons, selected candidate, ranking profile, policy version and timestamp.

## 9. Execution runtime

State machine:

`CREATED → POLICY_CHECK → QUEUED → STARTING → RUNNING → STREAMING → SUCCEEDED`

Terminal states:
`FAILED`, `CANCELLED`, `EXPIRED`, `DENIED`.

Required:
- durable execution ID
- idempotency key
- timeout
- cancellation
- bounded retries
- fallback attempts
- artifacts
- structured events
- provider correlation ID
- trace ID
- estimated/actual cost

Retry only transient errors such as 429/5xx/timeouts, subject to budget and provider policy.

Fallback is a separate attempt under the same logical execution and MUST be recorded.

## 10. Composition

Recipes are typed DAGs. MVP recipes MUST be acyclic.

Node types:
- capability/operation
- transformer
- validator

Transformer registry examples:
- PDF → text
- image → OCR text
- image → URL
- audio → transcript
- JSON → CSV
- resize/crop/format conversion

Planner pipeline:
`goal → output contract → capability search → candidate paths → transformers → graph validation → policy → cost/latency estimate → execution plan`.

MVP planner may only instantiate approved capabilities and recipes.

## 11. Artifact model

Artifact fields:
`artifact_id`, `type`, `mime`, `size`, `hash`, `storage_uri`, `created_by_execution`, `classification`, `retention`, `expires_at`, `metadata`.

Binary data belongs in object storage. Registry stores metadata.

Never move large binaries through model context when an artifact reference works.

## 12. Observability and economics

Trace:
`trace → execution → attempt → provider call → operation → artifact`.

Capture latency, status, usage units, provider, model/tool, cost, cache, retry, fallback, policy.

Health dimensions:
availability, p50, p95, error rate, queue delay, schema status, quota status, last success.

Before execution:
`estimated_min`, `estimated_expected`, `estimated_max`.

After execution:
`actual_provider_cost`, `platform_cost`, `total_cost`, `margin`.

Never invent provider prices.

## 13. API planes

### Discovery API
- `GET /v1/capabilities`
- `GET /v1/capabilities/{id}`
- `POST /v1/capability-search`

### Capability API
- `GET /v1/capabilities/{id}/implementations`
- `GET /v1/tools/{id}/contract`

### Execution API
- `POST /v1/executions`
- `GET /v1/executions/{id}`
- `POST /v1/executions/{id}/cancel`
- `GET /v1/executions/{id}/events`

### Composition API
- `POST /v1/recipes/validate`
- `POST /v1/recipes/plan`
- `POST /v1/recipes/execute`

All responses include `request_id`, `trace_id`, `data` or `error`.

Use cursor pagination. Breaking changes require new major API version.

## 14. MCP and A2A

Approved capabilities may be exported as MCP tools.

Remote MCP tools are imported as candidate interfaces and must pass schema/trust/policy evaluation.

A2A agents remain distinct from Tools. Adapter maps agent discovery/task lifecycle without collapsing an agent into an atomic function.

## 15. Channels and widget runtime

Do not build direct iframe dependencies as the core deployment model.

Preferred architecture:

`Browser → Widget Runtime → scoped session token → Execution API → routers → provider`

Provider credentials NEVER reach browser clients.

Modes:
- iframe
- Web Component
- JS SDK
- direct API

Channel classes:
- embedded UI: Web, Telegram Mini App, Discord Embedded App, Teams tab, LINE LIFF
- bot-native: Telegram bot, Slack, WhatsApp, Google Chat, GitHub, Linear, etc.

Every adapter declares auth, file support, streaming, interaction limits, HTTPS/CSP requirements and payload constraints.

SEO pages should contain real indexable content; widget is interactive layer, not the whole page.

## 16. Data connectors

Normalized operations:
`list`, `get`, `search`, `read`, `write`, `watch`, `delete`.

Possible adapters:
GitHub, Drive, Notion, Airtable, Postgres, S3-compatible storage, WordPress, Telegram, RSS/web.

Connector permissions are separate from tool permissions.

## 17. MVP implementation order

### P0
1. repository discipline
2. canonical domain
3. PostgreSQL schema/migrations
4. HF ingestion
5. Gradio/OpenAPI extraction
6. contract validation
7. evaluator
8. execution gateway
9. artifact storage
10. web widget

### P1
11. capability search/router
12. health/drift
13. cost engine
14. compatibility engine
15. transformers
16. recipes
17. Telegram adapter

### P2
18. Replicate/fal adapters
19. generic OpenAPI adapter
20. MCP import/export
21. A2A adapter
22. document pipeline
23. data connectors

### P3
24. constrained planner
25. multi-tenant product layer
26. billing abstraction
27. UI synthesis
28. autonomous discovery/planning

## 18. What NOT to build initially

Do not build your own:
- LLM
- vector database
- graph database
- browser engine
- Kubernetes platform
- billing processor
- giant agent swarm
- 20 channel adapters

Integrate where appropriate. Own the canonical contracts, evidence, policy, capability intelligence and provider-neutral execution semantics.

## 19. Deep implementation TODO

### Registry
- [ ] immutable IDs/versions
- [ ] tenant isolation
- [ ] deprecation model
- [ ] lifecycle transitions
- [ ] relational integrity

### Contracts
- [ ] canonical semantic type registry
- [ ] JSON Schema validation
- [ ] event envelope
- [ ] artifact schema
- [ ] error taxonomy

### Discovery
- [ ] HF pagination
- [ ] raw snapshots
- [ ] parser versioning
- [ ] 429/backoff
- [ ] dead letters
- [ ] resumability

### Security
- [ ] SSRF tests
- [ ] egress allowlist
- [ ] upload validation
- [ ] secret rotation
- [ ] audit log
- [ ] privileged approval

### Runtime
- [ ] idempotency
- [ ] cancellation
- [ ] timeout
- [ ] bounded retry
- [ ] fallback
- [ ] durable events

### Quality
- [ ] contract fixtures
- [ ] smoke tests
- [ ] health probes
- [ ] benchmark datasets
- [ ] regression thresholds

### Intelligence
- [ ] semantic search
- [ ] compatibility engine
- [ ] transformer registry
- [ ] cost estimator
- [ ] routing profiles
- [ ] drift detector

## 20. Acceptance criteria

AT-01 discovery stores raw + normalized + provenance.

AT-02 contract extraction produces deterministic operation schemas.

AT-03 schema drift creates a new immutable contract version and blocks incompatible execution.

AT-04 SSRF/private-network access is denied by default.

AT-05 duplicate idempotency request does not create duplicate logical execution.

AT-06 invalid candidates are excluded before scoring.

AT-07 fallback creates a distinct attempt with reason.

AT-08 compatible recipe validates; incompatible recipe fails unless a registered transformer exists.

AT-09 browser never receives provider secrets.

AT-10 tenant A cannot access tenant B execution/artifact/credential.

## 21. Weak-model implementation protocol

A coding model MUST receive a bounded task, target files, exact acceptance criteria and test command.

Before coding it reads:
- relevant spec
- relevant schema
- relevant ADR
- acceptance test

After coding it reports:
- changed files
- tests run
- failures
- assumptions
- unresolved VERIFY/TODO
- security impact
- migration impact

Reject code that:
- collapses Tool and Capability
- puts secrets in frontend
- bypasses policy
- retries everything
- mutates immutable versions
- hardcodes provider fields into core
- executes discovered resources without trust promotion
- invents pricing/capabilities
- claims unsupported channel compatibility

## 22. Production gates

Production requires:
- backup + restore test
- queue recovery
- provider outage test
- SSRF/security suite
- tenant isolation suite
- secret rotation
- schema drift test
- cost controls
- observability
- alerting
- incident runbook
- source/license review
- data retention review

No production launch based solely on model confidence or passing unit tests.

## 23. Source/verification basis

The supplied research document is the primary basis. It explicitly documents HF Spaces discovery, Gradio API/OpenAPI/agents.md, MCP, provider abstraction, recipes, channel adapters, risks, MVP, HF Inference Providers and Responses API, while also marking live inventory, exact limits, licensing, channel feasibility, competitor maturity and provider economics as areas requiring further verification.

Therefore this specification deliberately contains VERIFY gates rather than inventing provider behavior.
