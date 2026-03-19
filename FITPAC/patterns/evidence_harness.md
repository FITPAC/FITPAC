# Testing & Evidence Harness (Compressed)
# ID: evidence_harness
# Module key (for fragment IDs): `evidence_harness` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Satisfaction owns rubric (satisfaction.p3); evidence_harness owns generation and falsification.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Scenario Generators
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: ScenarioTemplate (inputs, preconditions, expected probe), EvidenceProbe.
- Invariants: Generated scenarios MUST be runnable and produce pass/fail vs EvidenceProbe (evidence_harness.inv.1).
- Triggers: failed_test, spec_ambiguity.
- RULE: Define ScenarioTemplate. Generate instances (random, boundary, equivalence). Run each; collect pass/fail; attach to EvidenceProbe.

## p2: Falsification Loop
```yaml
triggers: [falsification_loop]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: FalsificationLoop, property to falsify.
- Invariants: FalsificationLoop MUST stop when counterexample found and record it (evidence_harness.inv.2).
- Triggers: falsification_loop, failed_test.
- RULE: Define invariant or property. Generate candidate inputs; run; check property. On first failure record counterexample and stop. Report for triage.

## p3: Tests Against Invariants and Contracts
```yaml
triggers: [tests_tautological_or_nondeterministic]
requires_primitives: [Entity, Authority]
output_type: constraint
cross_refs: [ontology.p4, boundaries.p1]
domain: core
category: boundary
```

- RULE: Require tests against invariants (ontology.p4) and external boundary contracts, not just internal implementation. Boundary contract dictates what must be integration-tested (boundaries.p1).
- Triggers: failed_test, spec_ambiguity. Prevents tautological tests that mirror wrong code.

## p4: Fuzz Required
```yaml
triggers: [tests_tautological_or_nondeterministic]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- RULE: Fuzz required for specified surfaces: parsers, decoders, protocol handlers. Generate adversarial and boundary inputs; no narrow examples only.
- Triggers: failed_test, spec_ambiguity.

## p5: Test Temporal Containment
```yaml
triggers: [tests_tautological_or_nondeterministic]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- RULE: Tests MUST NOT rely on real time or sleep(); use fake clocks, deterministic schedulers. Prevents nondeterministic tests and timing-dependent assertions.
- Triggers: failed_test.
