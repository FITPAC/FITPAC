# Pattern languages

The FITPAC distribution ships with **30 pattern modules** under `patterns/`. Each pattern module is a **pattern language** module: a set of **sequentially numbered rules** (p1, p2, p3, …). Every rule has a YAML metadata block with **required fields** (`triggers`, `requires_primitives`, `output_type`, `domain`, `category`) and optional fields (`produces`, `cross_refs`), plus prose sections drawn from a **small, closed control vocabulary** (`REQUIRE`, `RULE`, `EMIT`, `NOTE`). Pattern format and indexing are defined normatively in [docs/reference/pattern-index.md](../reference/pattern-index.md) and the spec‑level control grammar in [docs/reference/spec-schema.md](../reference/spec-schema.md).

The **primitive spine** (`00_primitive_spine.md`) is a separate reference document at the FITPAC root; it is not a pattern module and has no numbered rules. These 30 pattern modules are the **base pattern set** that ships with this repository. Implementations MAY layer in additional pattern packs from other sources and MAY define local pattern modules of their own, as long as they follow the same pattern format and naming rules (module keys, fragment IDs, triggers) described in the reference docs.

### Control grammar for pattern bodies

Pattern bodies follow the same control grammar as specs:

- `REQUIRE` — Preconditions, invariants, and obligations the pattern introduces or relies on.
- `RULE` — Operational rules and control flow the orchestrator or agent should follow.
- `EMIT` — Outputs, events, or artifacts produced by applying the pattern.
- `NOTE` — Non‑normative explanation; safe to ignore for structural comparison.

Implementations MUST NOT introduce new section labels that carry normative behavior without updating the reference docs; additional headings are allowed only for readability and must be treated as comments.

## Core modules (in master_index pattern_map)

| Module | File | Role |
|--------|------|------|
| security | security_trust.md | Non-negotiable invariants, capability minting, delegation, IO contracts, SSRF, redaction, safe deserialization |
| ontology | domain_ontology.md | Semantic spine, state legality, invariant registry, ontology mapping, write owner, spec ambiguity/proposal |
| boundaries | boundary_contracts.md | contract.yaml, error taxonomy, retry budget, temporal containment, partial-failure policy |
| satisfaction | satisfaction_goals.md | Goals, evidenced validation, satisfaction rubric, state-model validation |
| ux | ui_ux.md | Impact-simulated preview, command graph |
| temporal | temporal.md | Idempotency, deadlines, sagas, leases, transaction boundary, time source, bounded concurrency |
| obs | obs.md | Trace context, probes, causal logging |
| budgets | budgets.md | Latency/cost tradeoffs, consult depth |
| schema_evolve | schema_evolve.md | Versioning, deprecation, compatibility, migration |
| deps_trust | deps_trust.md | Pinning, sandbox |
| resilience | resilience.md | Circuit breaker, reconciliation, rollback |
| governance | governance.md | Approval tiers, freeze, override |
| containment | containment.md | Speculation boundaries, source-required claims |
| evidence_harness | evidence_harness.md | Scenario generators, falsification, tests vs invariants/contracts, fuzz, test clocks |

## Primitive spine (reference document)

- **00_primitive_spine.md** (at the FITPAC root) — Single reference for Layer 1 (Entity, Transformation, Constraint, Authority, Relation, Context, Time) and Layer 2 (Transaction, Boundary, Projection, Capability, Policy) primitives; core semantics (execution and constraint evaluation); and aliases (Actor=Authority, Resource=Entity, Event=Transformation). This file is the **primitive spine** reference document; it is not a pattern module and does **not** define numbered `p1/p2/...` rules.

## Additional domains

These pattern files extend coverage. For prose→spec, implementations match prose to pattern triggers and category; for spec→code, `master_index.yaml` **pattern_map** lists which modules are loaded on demand:

- accessibility.md, api_design.md, compliance_audit.md, configuration.md, data_persistence.md, deployment.md, distributed_systems.md, error_handling.md, internationalization.md, messaging.md, ml_ai_systems.md, networking.md, performance.md, privacy_data_protection.md, spec_code_roundtrip.md, workflow_orchestration.md

## Module naming conventions, aliases, invariants, and triggers

For indexing, fragment IDs, and precedence, modules are identified by a **canonical module key**. This key is:

- the key in `master_index.yaml.pattern_map`, and
- the `<module>` portion of fragment IDs (`<module>.pN` and `<module>.inv.N`).

Common canonical module keys include:

- Core modules and their precedence ordering are as defined by `master_index.yaml` (see [Master index reference](../reference/master-index.md)); the reference distribution includes 30 canonical pattern modules under `FITPAC/patterns/`.
- Additional domains: `internationalization`, `accessibility`, `error_handling`, `privacy_data_protection`, `spec_code_roundtrip`, `configuration`, `deployment`, `distributed_systems`, `messaging`, `ml_ai_systems`, `networking`, `performance`, `compliance_audit`, `data_persistence`, `workflow_orchestration`, `api_design`.

Some pattern files use **short aliases** in their headers (`ID`) or `domain` fields. These aliases are for human readability only; fragment IDs always use the canonical module key. Examples:

- `internationalization` (module key)  
  - File: `internationalization.md`  
  - Typical alias: `i18n` (header `ID` and `domain`).
- `accessibility`  
  - File: `accessibility.md`  
  - Typical alias: `a11y`.
- `error_handling`  
  - File: `error_handling.md`  
  - Typical alias: `errors`.
- `privacy_data_protection`  
  - File: `privacy_data_protection.md`  
  - Typical alias: `privacy`.
- `spec_code_roundtrip`  
  - File: `spec_code_roundtrip.md`  
  - Typical alias: `roundtrip`.
- `configuration`  
  - File: `configuration.md`  
  - Typical alias: `config`.
- `data_persistence`  
  - File: `data_persistence.md`  
  - Typical alias: `persistence`.
- `workflow_orchestration`  
  - File: `workflow_orchestration.md`  
  - Typical alias: `workflow`.
- `distributed_systems`  
  - File: `distributed_systems.md`  
  - Typical alias: `distributed`.
- `compliance_audit`  
  - File: `compliance_audit.md`  
  - Typical alias: `compliance`.
- `api_design`  
  - File: `api_design.md`  
  - Typical alias: `api`.
- `ml_ai_systems`  
  - File: `ml_ai_systems.md`  
  - Typical alias: `ml_ai`.

This list is illustrative, not exhaustive; future modules may introduce similar aliases, but:

**Normative rule (modules and fragments):** In all fragment IDs (e.g. `internationalization.p1`, `spec_code_roundtrip.p3`) and invariant references (e.g. `ontology.inv.1`), the `<module>` portion MUST be a canonical module key from `master_index.yaml.pattern_map`. Header `ID` and per-rule `domain` aliases are for humans only and MUST NOT be used as the `<module>` part of these identifiers.

### Invariant identifiers

Some pattern rules introduce **named invariants**. When the library defines a stable invariant that may be referenced from specs, tests, or other patterns, it uses the naming convention:

- **`<module>.inv.N`** — for example, `api_design.inv.1`, `temporal.inv.1`, `privacy_data_protection.inv.4`. The `<module>` part MUST be the canonical module key from `pattern_map`.

These identifiers behave as follows:

- They are **attached to patterns and modules**, not maintained in a single global registry.
- FITPAC core modules (those in `master_index.yaml.pattern_map`) MAY define stable `X.inv.N` identifiers for important, reusable invariants.
- Project- or organization-specific patterns MAY:
  - define invariants only in prose, or
  - introduce project-local identifiers, without ever registering them globally.

Implementations are free to build **derived indexes** over invariants (by module, by affected entity, by severity, etc.), but those indexes are **non-normative**. The normative surface is:

- the pattern rules and their metadata (`triggers`, `requires_primitives`, `output_type`, `domain`, `category`, optional `produces`, `cross_refs`), and
- any invariant IDs a spec or pattern chooses to expose (e.g. `api_design.inv.1`).

### Trigger taxonomy (normative)

The `triggers` field in rule metadata is constrained by the **trigger and condition taxonomy** in `docs/reference/trigger-taxonomy.md`:

- Core triggers (e.g. `on_write`, `on_read`, `on_deadline`, `on_error:timeout`, `precondition:authority`, `invariant:state_legality`) MUST use the unnamespaced forms defined there.
- Domain‑specific triggers MUST use a namespaced form of the shape `<module>:<name>[:<qualifier>]`, where `<module>` is a canonical module key from `master_index.yaml.pattern_map` (e.g. `messaging:queue_backlog_high`, `ml_ai_systems:model_drift_detected`, `accessibility:contrast_ratio_low`).

When adding or updating rules:

- Prefer existing taxonomy entries wherever possible instead of inventing new spellings.
- If a new namespaced trigger is required, document it in the corresponding module’s file and keep semantics stable once published.

## Source

All pattern files live in the repo under [patterns/](https://github.com/FITPAC/fitpac-patterns/tree/main/patterns). For verbose descriptions of each rule, open the corresponding `.md` file in the repository.

### Contributor guidance

When adding new rules or modules, always:

- Use canonical module keys from `master_index.yaml.pattern_map` for any `X.pN` or `X.inv.N` identifiers (including in prose examples and `cross_refs`).
- Keep header `ID` and per-rule `domain` aliases strictly human-facing; never treat them as canonical identifiers in tooling or fragment IDs.

#### Authoring checklist (normative)

For each new rule:

1. **Metadata completeness**
   - `triggers` are present and drawn from the canonical trigger taxonomy or a documented namespaced extension.
   - `requires_primitives` reference only primitives from `00_primitive_spine.md`.
   - `output_type`, `domain`, and `category` are set and consistent with similar rules in the module.
2. **Good pattern hygiene**
   - `triggers` are specific enough to avoid matching unrelated prose, but not so narrow that they fragment the taxonomy (prefer `on_error:transient` over spelling variants).
   - `cross_refs` are used when this rule depends on or specializes another rule; avoid unnecessary cross‑module references.
   - If the rule introduces a reusable constraint, consider whether it should expose a named invariant (`<module>.inv.N`).
3. **Invariants and naming**
   - Only mint `X.inv.N` identifiers for invariants that are expected to be reused across specs, tests, or modules.
   - Document the meaning of each invariant close to its introducing rule, and keep the identifier stable once published.
   - For project‑local or experimental invariants, prefer spec‑local names or prose descriptions over global IDs.

Pattern linters and authoring tools SHOULD implement this checklist directly, treating missing required metadata or off‑taxonomy triggers as errors, and invariant naming issues as warnings.
