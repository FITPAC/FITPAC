# Model Containment (Compressed)
# ID: containment
# Module key (for fragment IDs): `containment` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Ontology governs domain meaning; containment governs speculation and provenance.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Speculation Boundary
```yaml
triggers: [speculation_without_source]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: SpeculationBoundary.
- Invariants: Content inside boundary MUST NOT be committed as fact without leaving boundary and satisfying SourceRequiredClaim (containment.inv.1).
- Triggers: speculation_without_source.
- RULE: Mark speculative or model-generated blocks as SpeculationBoundary. Output is draft until verified. Commit only after verification or explicit SourceRequiredClaim with provenance.

## p2: Source-Required Claim
```yaml
triggers: [speculation_without_source]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: SourceRequiredClaim, provenance (document, line, timestamp, or hash).
- Invariants: Every SourceRequiredClaim MUST have provenance (containment.inv.2).
- RULE: For claims affecting state or decisions require SourceRequiredClaim. Store provenance. If missing treat as unverifiable; RefuseWithExplanation or DeferToHigherTier.

## p3: Spec as Source of Truth and Traceability
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- RULE: Treat spec as source of truth; generated code MUST reference spec IDs (e.g. requirement id, pattern fragment id) for traceability. Prevents documentation drift and wrong assumptions.
- Triggers: spec_ambiguity, speculation_without_source.
