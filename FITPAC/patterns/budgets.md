# Optimization & Cost Budgets (Compressed)
# ID: budgets
# Module key (for fragment IDs): `budgets` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Correctness from ontology/satisfaction; budgets constrain choice only.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Tradeoff Grammar
```yaml
triggers: [budget_exceeded]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: LatencyBudget, CostBudget.
- Invariants: If LatencyBudget set, response within budget or return timeout (budgets.inv.1).
- Triggers: multi_valid_paths, budget_exceeded.
- RULE: If multiple valid paths, rank by LatencyBudget and CostBudget. Select first path that fits both. If none, fail with budget_exceeded; list options.

## p2: Consult Depth
```yaml
triggers: [budget_exceeded]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: ConsultDepthLimit, IterationCap.
- Invariants: Agent MUST stop consulting after ConsultDepthLimit; MUST stop iteration after IterationCap (budgets.inv.2).
- Triggers: budget_exceeded.
- RULE: Before each pattern consultation increment depth. If depth > ConsultDepthLimit do not load more fragments; apply SafeFallback or RefuseWithExplanation. EMIT: ConsultDepthReached.
