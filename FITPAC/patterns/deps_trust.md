# External Dependency Trust (Compressed)
# ID: deps_trust
# Module key (for fragment IDs): `deps_trust` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Security owns capability model; deps_trust owns external artifact/execution trust.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Pinning
```yaml
triggers: [dependency_unpinned]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: Dependency, Pin (version, hash, or lockfile).
- Invariants: Only Pinned dependencies MAY be used in production (deps_trust.inv.1).
- Triggers: dependency_unpinned, security_risk_detected.
- RULE: List all external dependencies. Each MUST have Pin. Build/deploy MUST fail if Pin missing or mismatch. On dependency_unpinned consult and fix before proceed.

## p2: Sandbox
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: Sandbox (network policy, timeout, resource limit).
- Invariants: Unpinned or untrusted external calls MUST go through Sandbox (deps_trust.inv.2).
- RULE: Identify boundaries that call external systems. Run in Sandbox. Log all sandboxed calls with outcome.
