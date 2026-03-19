# UI/UX Ergonomics (Compressed)
# ID: ux
# Module key (for fragment IDs): `ux` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Accessibility and internationalization extend interface design; this governs ergonomics and user experience.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Impact-Simulated Preview
```yaml
triggers: [irreversible_action, approval_required]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: other
```

- REQUIRE: Tiered Blast Radius summary before irreversible commit.
- GATE: Commit button inactive until impact computed.

## p2: Command Graph
```yaml
triggers: [irreversible_action]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: other
```

- REQUIRE: Machine-readable schema (JSON/YAML) for all UI actions.
- AGENTS: Use deterministic command strings, not visual scraping.
