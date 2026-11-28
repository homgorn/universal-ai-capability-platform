# Feature Specification: Widget Runtime (MVP-4)

**Branch**: `008-widget-runtime` | **Date**: 2026-11-28 | **Status**: Draft

## User Scenarios
### US1 - Scoped session token (P1)
A browser requests a widget; the runtime issues a short-lived scoped token bound to tenant,
tool and channel. Provider secrets never reach the browser.

### US2 - Channel constraint contract (P1)
Each channel adapter declares auth, file support, streaming, interaction limits, HTTPS/CSP and
payload constraints; incompatible requests are denied before execution.

### US3 - Modes (P2)
iframe, Web Component and JS SDK modes all resolve to the same Execution API contract.

### Edge cases
- Expired token → AUTH_REQUIRED, no execution.
- Channel that forbids files → ARTIFACT_UNSAFE/INVALID_INPUT before provider call.
- Unknown tool → 404, no token issued.

## Requirements
- FR-001: issue scoped, short-lived session tokens (tenant+tool+channel).
- FR-002: provider secrets MUST NOT appear in token or browser payload.
- FR-003: every channel adapter declares a constraint contract.
- FR-004: incompatible channel requests are denied pre-execution.
- FR-005: modes iframe/web-component/js-sdk share one Execution API contract.
- FR-006: token expiry and revocation are enforced.

## Success Criteria
- SC-001: 0 provider secrets in any browser-facing payload.
- SC-002: 100% channel requests checked against constraints.
- SC-003: expired token yields 0 executions.

## RU
MVP-4: scoped short-lived токен (tenant+tool+channel), секреты провайдеров не попадают в браузер;
контракт ограничений канала; iframe/web-component/js-sdk → единый Execution API.