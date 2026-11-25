# Mandatory Invariants

Eight invariants are non-negotiable: Tool != Capability; Resource != Interface; Capability Router != Provider Router; discovered != executable; historical contracts are immutable; provider secrets never reach browser; all external execution passes policy; every behavior has tests.

**RU:** Восемь инвариантов неизменны: Tool ≠ Capability; Resource ≠ Interface; Capability Router ≠ Provider Router; discovered ≠ executable; исторические контракты неизменяемы; секреты провайдеров не попадают в браузер; всё внешнее исполнение проходит policy; у каждого поведения есть тесты.

## Key Facts

- **Tool != Capability**: executable implementation vs semantic function
- **discovered != executable**: trust promotion required
- **historical contracts immutable**: append-only versions

## Table

| # | Invariant |
|---|---|
| 1 | Tool != Capability |
| 2 | Resource != Interface |
| 3 | Capability Router != Provider Router |
| 4 | discovered != executable |
| 5 | historical contracts are immutable |
| 6 | provider secrets never reach browser |
| 7 | all external execution passes policy |
| 8 | every behavior has tests |

## Sources

- AGENTS.md
- docs/SPECS.md §21
