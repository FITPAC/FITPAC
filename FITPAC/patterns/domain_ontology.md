# Domain Model & State (Compressed)
# ID: ontology
# Module key (for fragment IDs): `ontology` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Primitive spine defines core semantics; this governs domain vocabulary and state modeling.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Semantic Spine
```yaml
triggers: []
requires_primitives: [Entity, Authority, Constraint]
output_type: mapping
domain: core
category: domain
```

- "Semantic Spine" here refers to the **ontology mapping** (domain terms → primitives), not execution semantics; execution semantics (how transformations are executed, how constraints are evaluated) are defined in [00_primitive_spine.md](../00_primitive_spine.md).
- Primitives: Actor, Resource, Event, Capability, Policy.
- All domain terms MUST map to these via p5.

## p2: Delegation and Actor Scope
```yaml
triggers: [privilege_escalation]
requires_primitives: [Entity, Authority, Constraint]
output_type: constraint
cross_refs: [security.p3]
domain: core
category: domain
```

- Actor scope and delegation chain MUST be explicit for Policy checks.
- Used with security.p3 for privilege_escalation (depth, loop, cross-boundary).

## p3: Constructive State Legality
```yaml
triggers: [invalid_state_transition]
requires_primitives: [Entity, Authority, Constraint]
output_type: constraint
domain: core
category: invariant
```

- Illegal states MUST be unrepresentable.
- Reject events that trigger undefined (State, Event) transitions.

## p4: Global Invariant Registry
```yaml
triggers: [missing_invariant]
requires_primitives: [Entity, Authority, Constraint]
output_type: constraint
domain: core
category: invariant
```

- Check registry BEFORE commit.
- Failure = RejectEvent.

## p5: Ontology Mapping Contract
```yaml
triggers: [unknown_domain_term, conflicting_mappings]
requires_primitives: [Entity, Authority, Constraint]
output_type: mapping
domain: core
category: domain
```

- Domain terms (e.g. 'Deployment') must have explicit mapping to Primitives.
- No mapping = UnknownDomainTerm ambiguity.

## p6: Conflicting Mappings
```yaml
triggers: [conflicting_mappings]
requires_primitives: [Entity, Authority, Constraint]
output_type: decision
domain: core
category: domain
```

- Same term maps to different Primitives or semantics across contexts = conflicting_mappings.
- DECISION: Resolve by scope (prefer narrower scope) or RefuseWithExplanation.
- DOCUMENT: Chosen mapping and scope in SpecProposal or inline; avoid duplicate definitions.

## p7: Spec Ambiguity Handling
```yaml
triggers: [unknown_domain_term, missing_invariant, spec_ambiguity]
requires_primitives: [Entity, Authority, Constraint]
produces: SpecAmbiguityDetected
output_type: decision
domain: core
category: domain
```

- IF ambiguous: Classify (UnknownTerm, Conflict, MissingInvariant).
- RESPOND: RefuseWithExplanation | DeferToHigherTier | ExecuteSafeFallback.
- EMIT: `SpecAmbiguityDetected` event.

## p8: Spec Negotiation & Proposal
```yaml
triggers: [spec_ambiguity]
requires_primitives: [Entity, Authority, Constraint]
produces: SpecProposal
output_type: decision
domain: core
category: domain
```

- IF authorized: Propose new mapping/invariant via `SpecProposal`.
- REQUIRE: Evidence + Impact Assessment.

## p9: Write Owner and Mutation Authority
```yaml
triggers: [write_ownership_unspecified]
requires_primitives: [Entity, Authority, Constraint]
produces: WriteOwnerConstraint
output_type: constraint
cross_refs: [security.p3]
domain: core
category: ownership
```

- Every mutable Resource MUST have an explicit write owner (Actor or service boundary).
- Spec hook: "Who may mutate which resource?" Prevents split-brain, duplicate writes, phantom updates.
- RULE: Declare write owner per resource type; reject mutations from non-owner unless delegated (security.p3).

## p10: First-Class Spec Fields (Idempotency, Uniqueness, Ordering)
```yaml
triggers: [implicit_constraints_omitted]
requires_primitives: [Entity, Authority, Constraint]
output_type: constraint
cross_refs: [temporal.p1]
domain: core
category: invariant
```

- When operations can repeat or overlap: REQUIRE IdempotencyKey in spec (temporal.p1).
- When uniqueness matters: REQUIRE uniqueness keys or constraints in spec; no "create X" without uniqueness.
- When order matters: REQUIRE explicit ordering guarantees (per-key vs global) in spec.
- Spec hook: Prevents duplicates, double billing, repeated side effects; use with temporal and boundaries.
