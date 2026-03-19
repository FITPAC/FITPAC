# Schema Evolution & Compatibility (Compressed)
# ID: schema_evolve
# Module key (for fragment IDs): `schema_evolve` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Ontology governs meaning; this governs version and compatibility.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Versioning
```yaml
triggers: [schema_version_mismatch]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: SchemaVersion.
- Invariants: Clients within DeprecationWindow MUST be accepted (schema_evolve.inv.1).
- Triggers: schema_version_mismatch, spec_ambiguity.
- RULE: All APIs/configs declare SchemaVersion. On request read client version. If supported, process. If deprecated but in window, process and add deprecation header. If out of window, reject (410 or equivalent).

## p2: Deprecation
```yaml
triggers: [schema_version_mismatch]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: DeprecationWindow, Migration.
- Invariants: After DeprecationWindow deprecated path MUST be rejected with clear error (schema_evolve.inv.2).
- RULE: Declare deprecation date and DeprecationWindow (e.g. 90 days). Document Migration path. After window remove or reject deprecated path.

## p3: Compatibility Rules
```yaml
triggers: [schema_version_mismatch]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- RULE: Additive-only new fields where possible; reserved enum values for future; tolerant readers (ignore unknown fields). Document backwards/forwards compatibility strategy.
- Triggers: schema_version_mismatch, spec_ambiguity.

## p4: Migration Playbook
```yaml
triggers: [schema_version_mismatch]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- RULE: Migrations follow expand/contract or dual-write; verify backfill; no long-running locks, no non-null assumption before backfill complete. Document ordering and verification steps.
- Triggers: schema_version_mismatch (migration bugs).
