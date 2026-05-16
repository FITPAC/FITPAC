---
title: Pattern index reference
status: normative-reference
implements: RFC-0005
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
copyright_holder: Paul Roy and FITPAC Contributors
attribution_note: Attribution required under CC BY 4.0.
---

# Pattern index reference

The reference distribution ships with **30 canonical pattern modules** under `FITPAC/patterns/`; these are the normative default for the Reference Profile. Other patterns may be added (e.g. organizational packs); the canonical set is fixed for a given FITPAC version.

### Extension pattern modules (RFC-0006)

The **`fitpac.prose_compiler`** extension adds one RFC-0005 module for the **prose→primitives** pipeline:

| Module key | File | Fragments |
|------------|------|-----------|
| `fitpac.prose_compiler` | `FITPAC/extensions/fitpac_prose_compiler/patterns/fitpac_prose_compiler.md` | `fitpac.prose_compiler.p1` (clause typing) … `fitpac.prose_compiler.p6` (resolution) |

Registration: [`extension-registry.md`](extension-registry.md), [`extensions/extension_registry.yaml`](../../extensions/extension_registry.yaml). Resolve paths with `python3 FITPAC/tools/fitpac_prose_compiler_context.py`.

For the **prose→spec** pipeline (core patterns), each pattern is described by metadata in its YAML block (in `patterns/*.md`). Implementations may build a flat index from the pattern files with:

- **id** — e.g. `security.p1`, `ontology.p5`
- **title** — Short name of the pattern
- **triggers** — List of trigger keywords that match this pattern (used for retrieval)
- **output_type** — e.g. constraint, policy, decision, mapping
- **cross_refs** — Other pattern IDs this pattern references
- **requires_primitives** — Primitives required (e.g. Entity, Authority)
- **produces** — Optional. Artifact or event this rule produces (e.g. SpecAmbiguityDetected, SpecProposal, WriteOwnerConstraint).
- **domain** — e.g. core, a11y, messaging
- **category** — security | invariant | ownership | domain | boundary | other (used for **sort order in retrieval**, not for value hierarchy)

**Retrieval:** The orchestrator matches user prose (or keywords/embeddings) against pattern `triggers`, then:

- filters by other metadata as needed (e.g. `domain`),
- sorts matched IDs by **category** (security → invariant → ownership → domain → boundary → other) to surface safety‑critical and invariant rules first,
- loads only those pattern bodies from `patterns/*.md`, and
- injects them plus prose into the Socratic LLM.

This **category ordering is a retrieval hint only**. It does **not** encode the organization’s value hierarchy; global precedence between modules is defined solely by `precedence_hierarchy` in `master_index.yaml`.

---

## Pattern format (normative)

Each pattern file is a **pattern language** module composed of **sequentially numbered rules**:

- **Rule IDs:** Within a file, rules are numbered `p1, p2, p3, …`. Once a rule index `pN` has been published, it MUST NOT be renumbered; gaps MAY exist due to deprecation, but deprecated rules MUST remain present and clearly marked (e.g. `status: deprecated`). Fragments are referenced as `module.pN` (e.g. `security.p1`, `ontology.p5`).
- **YAML block per rule (required fields)** — these fields are present for **every** rule:
  - `triggers` — List of trigger keywords or conditions.
  - `requires_primitives` — List of primitives required (see `00_primitive_spine.md`).
  - `output_type` — One of: constraint, policy, decision, mapping, or another well-defined type.
  - `domain` — Module or domain name (e.g. core, api, persistence, networking, config).
  - `category` — One of: security | invariant | ownership | domain | boundary | other.
- **YAML block per rule (optional fields)** — these may be omitted when not needed:
  - `produces` — Artifact or event this rule produces (e.g. SpecAmbiguityDetected, SpecProposal, WriteOwnerConstraint).
  - `cross_refs` — Other pattern IDs this rule references (e.g. `security.p1`, `boundaries.p2`).

Primitive names used in `requires_primitives` MUST match the canonical primitives defined in `00_primitive_spine.md`.

In the current pattern library many rules omit `produces` and/or `cross_refs`; this is expected and compliant with the normative format.

These fields (`id`, `triggers`, `requires_primitives`, `output_type`, `domain`, `category`, and optional `produces`, `cross_refs`) constitute the **minimal normative grammar** for pattern rules. Implementations are free to build additional indexes or heuristics on top of this metadata (e.g. embeddings, usage frequency, custom scoring), but such indexes are **non‑normative** and MUST NOT change fragment IDs or the meaning of these fields.

---

## Parsing pattern files

Implementations that need to load individual rules (e.g. for fragment-on-demand loading) MUST parse pattern files as follows. This is the **normative structure** for machine-readable extraction; the generator script `FITPAC/tools/generate_master_index.py` follows it.

1. **Rule boundary:** Each rule is a level-2 Markdown heading of the form `## pN` or `## pN : Title` (where `N` is one or more digits). The heading defines the fragment ID suffix for that rule; the full fragment ID is `<module>.pN` where `<module>` is the key from `master_index.yaml.pattern_map` for this file.

2. **YAML block:** Immediately after the rule heading, the rule’s metadata MUST appear in a fenced code block. The opening fence MUST be ` ```yaml ` or ` ``` ` (with optional newline). The block continues until the closing ` ``` `. The block’s contents MUST be valid YAML; when parsed as a single document, it MUST yield a mapping containing at least the required fields (`triggers`, `requires_primitives`, `output_type`, `domain`, `category`).

3. **Rule body:** Any content after the closing fence and before the next `## pN` heading (or end of file) is the rule body. The body may be prose, bullet lists, or REQUIRE/RULE/EMIT/NOTE sections; it is the human- and agent-readable description of the rule. When loading “only the fragment” for a given `module.pN`, implementations typically load the heading, the YAML block, and the following body up to (but not including) the next `## pN` heading.

4. **Order:** Rules appear in sequential order (`p1`, `p2`, `p3`, …). Once published, indices MUST NOT be renumbered; gaps MAY exist due to deprecation, with deprecated rules remaining present and clearly marked. Only files under `patterns/` that define numbered rules are included in `pattern_map`; the primitive spine (`00_primitive_spine.md`) lives outside `patterns/` and has no fragment IDs.

Implementations that build indexes (e.g. from triggers to fragment IDs) SHOULD scan all `*.md` under the patterns directory, parse each rule heading and its YAML block, and key results by fragment ID and by the `triggers` (and optionally `domain`, `category`) fields for retrieval.

---

**Control vocabulary in rule bodies:** The control grammar (REQUIRE, RULE, EMIT, NOTE) defined in [spec-schema.md](spec-schema.md) applies normatively to **spec documents**. For **pattern rule bodies** in `patterns/*.md`, the same semantics may be expressed in free-form prose, bullet lists, or explicit REQUIRE/RULE/EMIT/NOTE headings. New patterns SHOULD use the control vocabulary where it improves clarity; existing pattern content that uses equivalent meaning in prose is **compliant**. Validators and linters MUST NOT treat pattern files as non-compliant solely because rule bodies use bullets or paragraphs instead of these section labels.

Normative rule for large libraries:

- Implementations SHOULD build **keyed indexes** for at least:
  - `id` (for direct lookup by `module.pN`),
  - `triggers` (for prose→pattern matching),
  - `requires_primitives` (for primitive‑driven retrieval),
  - `domain` and `category` (for coarse filtering).
- These indexes MAY be sharded by module, profile, or domain, but MUST present a stable logical surface: the meaning of a given `id` or `trigger` lookup is independent of how the index is physically stored.

---

## Module and fragment IDs

Fragment IDs have the form:

- **`<module>.pN`** — for example, `security.p1`, `ontology.p5`, `privacy_data_protection.p3`.

The **`<module>` part is the key from `master_index.yaml.pattern_map`**, not necessarily:

- the `ID` header at the top of the pattern file, or
- the `domain` field inside each rule’s YAML block.

Examples:

- `master_index.yaml.pattern_map.security` → `patterns/security_trust.md`  
  - Fragment IDs: `security.p1`, `security.p2`, …
  - File header `ID: security` and `domain: core` for rules.
- `master_index.yaml.pattern_map.internationalization` → `patterns/internationalization.md`  
  - Fragment IDs: `internationalization.p1`, `internationalization.p2`, …  
  - File header `ID: i18n`, rule `domain: i18n` (short alias).
- `master_index.yaml.pattern_map.accessibility` → `patterns/accessibility.md`  
  - Fragment IDs: `accessibility.p1`, `accessibility.p2`, …  
  - File header `ID: a11y`, rule `domain: a11y`.
- `master_index.yaml.pattern_map.error_handling` → `patterns/error_handling.md`  
  - Fragment IDs: `error_handling.p1`, …  
  - File header `ID: errors`, rule `domain: errors`.
- `master_index.yaml.pattern_map.privacy_data_protection` → `patterns/privacy_data_protection.md`  
  - Fragment IDs: `privacy_data_protection.p1`, …  
  - File header `ID: privacy`, rule `domain: privacy`.
- `master_index.yaml.pattern_map.spec_code_roundtrip` → `patterns/spec_code_roundtrip.md`  
  - Fragment IDs: `spec_code_roundtrip.p1`, …  
  - File header `ID: roundtrip`, rule `domain: roundtrip`.

**Normative rule:** when constructing or resolving fragment IDs, always use the **module key from `pattern_map`**. Header `ID` and `domain` fields may use shorter, human-oriented aliases but MUST NOT be used as the `<module>` part of fragment IDs.

---

## Primitive spine (reference document, not a pattern module)

The file `00_primitive_spine.md` lives at the FITPAC root (not under `patterns/`). It is the **primitive spine** reference document and is not a pattern module:

- It defines the **canonical primitives** (Entity, Transformation, Constraint, Authority, Relation, Context, Time) and structural primitives (Transaction, Boundary, Projection, Capability, Policy).
- It documents **core semantics** (execution semantics and constraint evaluation semantics) and common aliases (Actor=Authority, Resource=Entity, Event=Transformation).
- It does **not** define numbered rules (`p1`, `p2`, …) and has **no fragment IDs** of the form `module.pN`.

The rule-numbering requirements in this document apply only to pattern modules under `patterns/*.md`.

---

## Adding new modules (forward compatibility)

When extending the pattern library with new modules, follow these rules to preserve stability.

### Adding a new pattern module (checklist)

To add a new pattern module and wire it into the consultation flow:

1. **Add the pattern file** under `patterns/` with sequentially numbered rules (`p1`, `p2`, …), each with the required YAML fields (`triggers`, `requires_primitives`, `output_type`, `domain`, `category`). Use primitives from `00_primitive_spine.md` only. See [trigger-taxonomy.md](trigger-taxonomy.md) for trigger vocabulary.
2. **Update `master_index.yaml`:** Add the module key and filename to `pattern_map`. If the module participates in conflict resolution, add the same key to `precedence_hierarchy` at the desired precedence level.
3. **Wire triggers (if needed):** If the new module should be consulted when specific conditions occur, add entries to `ambiguity_triggers` mapping each condition to the minimal list of fragments (e.g. `new_module.p1`, `new_module.p2`). Add a corresponding entry in `confidence_model.drop_conditions` with a delta (e.g. `-0.20`) for each new trigger key.

See also [master-index.md](master-index.md) ("Extending master_index.yaml safely") for fragment ID immutability and empty-fragment-list rules.

1. **Choose a stable module key**
   - Pick a canonical module key (e.g. `feature_flags`, `ml_ai_systems`, `data_quality`) that will be used as the `<module>` portion of fragment IDs.
   - Add this key and its filename to `master_index.yaml.pattern_map`.
   - If the module participates in conflict resolution, add the same key to `master_index.yaml.precedence_hierarchy`.

2. **Aliases are allowed, but fragment IDs use the module key**
   - You MAY use a shorter or domain-specific alias in:
     - the pattern file header `ID` (e.g. `ID: i18n`), and/or
     - the per-rule `domain` field (e.g. `domain: a11y`).
   - These aliases are **non-normative**; all fragment IDs MUST use the `pattern_map` key (`internationalization`, `accessibility`, etc.).

3. **Do not rename existing module keys or renumber rules**
   - Once a module key appears in `pattern_map`, treat it as **immutable**. Renaming it would change every fragment ID (e.g. `module.pN`) and break existing integrations.
   - Within a module, rule numbers (`p1`, `p2`, …) are likewise **stable** once published. To deprecate behavior:
     - leave old rules in place and document their status, and
     - add new rules (e.g. `pN+1`) or higher-precedence modules instead of removing or renumbering.

4. **Keep metadata complete**
   - Ensure each new rule has all **required** YAML fields (`triggers`, `requires_primitives`, `output_type`, `domain`, `category`).
   - Use `produces` and `cross_refs` where applicable to support deterministic retrieval and tooling, but do not fabricate values where they do not apply.

Following these rules lets the pattern language grow (new modules, new rules, new triggers) without breaking existing fragment IDs, indexes, or FITPAC-conformant implementations.
