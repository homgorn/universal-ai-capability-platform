# Feature Specification: Evaluator (MVP-3)

**Branch**: `007-evaluator` | **Date**: 2026-11-27 | **Status**: Draft

## User Scenarios
### US1 - Deterministic evidence-backed evaluation (P1)
A candidate tool is evaluated into independent dimensions (quality, reliability, latency,
cost, safety), each with an evidence mark. Missing evidence becomes VERIFY, never a number.

### US2 - No invented metrics (P1)
The evaluator MUST NOT fabricate prices, latency or quality. Unknown dimensions stay null +
VERIFY.

### US3 - Ranking profiles consume evaluations (P2)
Profiles QUALITY_FIRST / BALANCED / CHEAPEST_VALID / LOW_LATENCY / PRIVATE / SELF_HOSTED rank
candidates using only present, evidence-marked dimensions; missing dimensions never score as zero.

### Edge cases
- All dimensions unknown → candidate is VERIFY, not ranked.
- Conflicting evidence → lowest trust mark wins.
- License unknown → excluded from white-label profile.

## Requirements
- FR-001: store 5 independent dimensions, no single weighted score as truth.
- FR-006: every dimension has evidence_mark + observed_at.
- FR-007: unknown → null + VERIFY, never 0 or invented.
- FR-008: profile ranking ignores missing dimensions (does not penalize as zero).
- FR-009: license unknown excludes candidate from redistributable profiles.
- FR-010: evaluation is deterministic for identical inputs.

## Success Criteria
- SC-001: 0 invented numbers across fixtures.
- SC-002: 100% dimensions carry evidence marks.
- SC-003: ranking is stable for identical inputs.
- SC-004: unknown license never enters white-label top results.

## RU
MVP-3: детерминированная оценка кандидатов по 5 независимым измерениям с evidence mark;
неизвестное — null + VERIFY, не выдуманные числа; профили ранжирования игнорируют отсутствующие
измерения; неизвестная лицензия исключает из white-label.