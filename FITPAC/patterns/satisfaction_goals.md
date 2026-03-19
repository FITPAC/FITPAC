# Satisfaction & Scenarios (Compressed)
# ID: satisfaction
# Module key (for fragment IDs): `satisfaction` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Ontology and boundaries provide context; this governs goal-oriented behavior and scenario validation.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Goal-Oriented Trajectory
```yaml
triggers: [spec_ambiguity]
requires_primitives: [Entity, Authority]
output_type: decision
domain: core
category: domain
```

- Root: Goal. Unit: Trajectory (ordered scenarios).
- Score satisfaction, not just pass/fail.

## p2: Evidenced Validation
```yaml
triggers: [partial_failure]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: domain
```

- REQUIRE: Observable proof (direct_output, side_effect, log).
- RULE: Side-effect failure zeroes correctness even if direct_output succeeds.

## p3: Satisfaction Rubric
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: domain
```

- HARD ZERO: Security breach, Data corruption, Invariant violation.
- DIMENSIONS: Correctness, Clarity, Friction.

## p4: State Model Validation
```yaml
triggers: [invalid_state_transition]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: domain
```

- Scenarios MUST validate resulting state via evidence probes.
