# Specification-Code Roundtrip (Compressed)
# ID: roundtrip
# Module key (for fragment IDs): `spec_code_roundtrip` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Ontology provides semantic spine; containment governs speculation; this governs spec↔code translation fidelity.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Spec Element Traceability
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: roundtrip
category: other
```

- Primitives: SpecElement (id, type, content), CodeArtifact (file, line_range, element_refs).
- Invariants: Every CodeArtifact MUST reference at least one SpecElement ID (spec_code_roundtrip.inv.1).
- Triggers: traceability_violation, spec_ambiguity.
- RULE: During code generation, annotate each function/class/module with originating SpecElement IDs. Use comments, decorators, or metadata files. Traceability MUST survive refactoring.

## p2: Reverse Extraction Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: roundtrip
category: other
```

- Primitives: ExtractedSpec (from code analysis), CanonicalSpec (source of truth).
- Invariants: ExtractedSpec MUST be expressible in same grammar as CanonicalSpec (spec_code_roundtrip.inv.2).
- Triggers: reverse_extraction_failed, semantic_drift.
- RULE: Define extraction rules for each SpecElement type. Code patterns (e.g., validation, error handling, API signatures) map to spec constructs. If pattern unrecognized, emit UnmappedCodePattern warning.

## p3: Semantic Diff Classification
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: roundtrip
category: other
```

- Primitives: SemanticDiff (category: cosmetic | behavioral | contractual), DiffSeverity.
- Invariants: Contractual diffs MUST block iteration completion (spec_code_roundtrip.inv.3).
- Triggers: semantic_drift, convergence_stalled.
- RULE: Compare ExtractedSpec to CanonicalSpec. Classify differences:
  - Cosmetic: naming, formatting, comment changes → allow
  - Behavioral: logic changes within contract → flag for review
  - Contractual: API signature, invariant, boundary changes → reject
- When execution semantics are present in the spec, behavioral diffs should take them into account: same entities/transformations/constraints can yield different observable behavior under different execution models (e.g. state machine vs event-sourced).
- EMIT: SemanticDiffReport.

## p4: Convergence Criteria
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: roundtrip
category: other
```

- Primitives: ConvergenceCriteria (max_iterations, acceptable_drift, required_coverage).
- Invariants: Iteration MUST terminate when ConvergenceCriteria met OR max_iterations exceeded (spec_code_roundtrip.inv.4).
- Triggers: convergence_stalled, iteration_cap_exceeded.
- RULE: Define convergence as: zero contractual diffs, behavioral diffs below threshold, all SpecElements have corresponding CodeArtifacts. If not converged after max_iterations, escalate with DivergenceReport.

## p5: Code Generation Constraints
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: roundtrip
category: other
```

- Primitives: CodeStyle (language, idioms, patterns), GenerationConstraint.
- Triggers: style_violation, unmappable_spec.
- RULE: Declare target CodeStyle per project. Generated code MUST conform. If SpecElement cannot map to CodeStyle (e.g., language limitation), emit SpecCodeMismatch and propose alternatives or manual intervention.

## p6: Bidirectional Consistency Check
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: roundtrip
category: other
```

- Primitives: ConsistencyProof (spec_hash, code_hash, extraction_result).
- Invariants: If code modified without spec update, ConsistencyProof invalid (spec_code_roundtrip.inv.5).
- Triggers: consistency_broken, unauthorized_code_change.
- RULE: On every commit, re-extract spec from code and compare to canonical. If divergence detected without corresponding spec change, reject commit or flag for reconciliation.

## p7: Ambiguity Injection Points
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: roundtrip
category: other
```

- Primitives: AmbiguityMarker (location, question, options).
- Triggers: spec_ambiguity, spec_clarification_required.
- RULE: When spec contains ambiguity that affects code generation, inject AmbiguityMarker in generated code as TODO or placeholder. Do NOT guess. Collect all markers for human review before iteration proceeds.

## p8: Spec Coverage Metric
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: roundtrip
category: other
```

- Primitives: SpecCoverage (elements_mapped, elements_total, unmapped_list).
- Invariants: SpecCoverage MUST reach threshold before code considered complete (spec_code_roundtrip.inv.6).
- Triggers: incomplete_implementation.
- RULE: Track which SpecElements have corresponding CodeArtifacts. Report coverage percentage. Unmapped elements indicate incomplete implementation or spec elements requiring manual handling.
