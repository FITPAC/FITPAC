# Governance & Escalation (Compressed)
# ID: governance
# Module key (for fragment IDs): `governance` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Security owns capability minting; UX owns blast-radius preview; governance owns approval and freeze.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Approval Tiers
```yaml
triggers: [approval_required]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: ApprovalTier (e.g. automated, human_approval, multi_party).
- Invariants: Irreversible action MUST require at least defined ApprovalTier (governance.inv.1).
- Triggers: approval_required, irreversible_action.
- RULE: Classify actions by risk; assign ApprovalTier. Before irreversible action verify current tier >= required. If not block and request escalation or approval.

## p2: Freeze and Override
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: FreezeWindow, Override.
- Invariants: Override MUST be logged and auditable (governance.inv.2).
- RULE: FreezeWindow: during window no mutations to frozen scope. Override: only with Override token; audit log entry with reason and actor.

## p3: Behavioral Equivalence and Refactor Safety
```yaml
triggers: [refactor_without_equivalence]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- RULE: Before accepting large refactors require behavioral equivalence checks: golden tests, snapshots, or invariant checks. Require delete path and feature-flag retirement plan for dead code.
- Triggers: spec_ambiguity (large diff with subtle semantic change).
