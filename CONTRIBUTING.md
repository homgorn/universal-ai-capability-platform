# Contributing

Thanks for contributing to the Universal AI Capability Platform.

## Ground rules

- Implement from the relevant `specs/<feature>/spec.md`, `plan.md` and ADRs.
- Do not redesign architecture without an ADR.
- Tool != Capability; Resource != Interface; discovered != executable.
- Never put provider secrets in client code; never bypass policy.
- Every behavior needs a test.

## Workflow (GitHub Spec Kit)

1. `/speckit.constitution` — project principles.
2. `/speckit.specify` — WHAT/WHY, no tech stack.
3. `/speckit.plan` — architecture, stack, data model, contracts.
4. `/speckit.tasks` — ordered, testable tasks.
5. `/speckit.analyze` — cross-artifact consistency.
6. `/speckit.implement` — code + tests.

## Before opening a PR

```bash
cd backend
python scripts/health.py   # ruff + mypy + pytest must all pass
```

Report changed files, tests run, assumptions, unresolved VERIFY/TODO, security and migration impact.

## Languages

READMEs are maintained in English, Russian, Chinese, Spanish and German. Keep answer-first, fact-dense structure when editing them.