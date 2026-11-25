# Execution Runtime

Execution is a first-class durable entity. State machine: CREATED → POLICY_CHECK → QUEUED → STARTING → RUNNING → STREAMING → SUCCEEDED, with terminals FAILED, CANCELLED, EXPIRED, DENIED. Every execution has a durable ID, idempotency key, timeout, cancellation, bounded retries, fallback attempts, artifacts, structured events, provider correlation ID and trace ID. Only transient errors (429/5xx/timeouts) retry.

**RU:** Исполнение — первоклассная долговечная сущность. Конечный автомат: CREATED → POLICY_CHECK → QUEUED → STARTING → RUNNING → STREAMING → SUCCEEDED; терминалы — FAILED, CANCELLED, EXPIRED, DENIED. У каждого исполнения есть durable ID, ключ идемпотентности, таймаут, отмена, ограниченные повторы, fallback-попытки, артефакты, структурные события, provider correlation ID и trace ID. Повтор только для транзиентных ошибок (429/5xx/таймаут).

## Key Facts

- **Idempotency**: duplicate request does not create a duplicate logical execution
- **Fallback**: separate attempt under the same logical execution, recorded with reason

## Table

| State | Kind |
|---|---|
| CREATED | initial |
| POLICY_CHECK | gate |
| QUEUED | waiting |
| STARTING | provisioning |
| RUNNING | executing |
| STREAMING | streaming output |
| SUCCEEDED | terminal |
| FAILED / CANCELLED / EXPIRED / DENIED | terminal |

## Sources

- docs/SPECS.md §9
- contracts/execution-contract.yaml
