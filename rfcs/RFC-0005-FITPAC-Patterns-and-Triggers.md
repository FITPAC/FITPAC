---
RFC: 0005
Title: FITPAC Pattern and Trigger Grammar
Author: Paul Roy
Status: Final
Version: 1.0.0
Date: 2025-03-17
Depends-on:
  - RFC-0001
  - RFC-0003
  - RFC-0004
Supersedes: None
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
copyright_holder: Paul Roy and FITPAC Contributors
attribution_note: Attribution required under CC BY 4.0.
adoption_status: adopted
standard_inclusion: canonical-reference
---

# RFC-0005: FITPAC Pattern and Trigger Grammar

## 1. Scope

This document defines the normative **pattern module format**, **fragment ID rules**, and **trigger taxonomy** for FITPAC. RFC-0001 and RFC-0003 describe the primitives and control grammar; this RFC binds those concepts to the concrete pattern files under `FITPAC/patterns/*.md` and the trigger taxonomy in `FITPAC/docs/reference/trigger-taxonomy.md`.

The **canonical pattern set** for FITPAC 1.0.0 is the set of pattern modules shipped by default under `FITPAC/patterns/` (30 modules in the reference distribution). Other patterns MAY be added (e.g. organizational or domain packs); the canonical set is the normative default for the Reference Profile. Pattern module file names use **snake_case** per RFC-0001 §1.3 (e.g. `domain_ontology.md`, `boundary_contracts.md`).

---

## 2. Pattern Modules and Rule Structure

The detailed pattern format is implemented by the normative reference `FITPAC/docs/reference/pattern-index.md`. A FITPAC-conformant pattern library:

- **MUST** organize rules into pattern modules, each backed by a Markdown file under `FITPAC/patterns/`.
- **MUST** number rules sequentially within each module as `p1, p2, p3, …`. Once a rule index `pN` has been published, it **MUST NOT** be renumbered; gaps MAY exist due to deprecation, but deprecated rules MUST remain present and clearly marked (for example, with `status: deprecated` metadata as described in `pattern-index.md`).
- **MUST** provide, for each rule:
  - a level-2 heading (`## pN` or `## pN : Title`),
  - a YAML metadata block with required fields (`triggers`, `requires_primitives`, `output_type`, `domain`, `category`), and
  - an optional body expressed in prose and/or control grammar sections (REQUIRE, RULE, EMIT, NOTE).

Primitive names used in `requires_primitives` **MUST** match the canonical primitives defined in the primitive spine (RFC-0003 and `FITPAC/00_primitive_spine.md`).

---

## 3. Fragment IDs and Module Keys

Fragment IDs have the reference form:

- `<module>.pN` (for example, `security.p1`, `ontology.p5`, `privacy_data_protection.p3`).

Implementations:

- **MUST** derive the `<module>` portion from the canonical module key in `master_index.yaml.pattern_map`.
- **MUST NOT** use human-friendly aliases (for example, `a11y`, `i18n`, `errors`) as the `<module>` part of fragment IDs.
- **MUST** treat published fragment IDs and module keys as **immutable**; renaming module keys or renumbering rules is a breaking change.

The mapping from module keys to files is defined normatively by `FITPAC/master_index.yaml` and described in `FITPAC/docs/reference/pattern-index.md`.

---

## 4. Trigger and Condition Taxonomy

The trigger and condition vocabulary is defined by the normative reference `FITPAC/docs/reference/trigger-taxonomy.md`. Implementations:

- **MUST** draw `triggers` entries in rule metadata from:
  - the core trigger list (unnamespaced form), or
  - documented namespaced extensions (for example, `messaging:queue_backlog_high`, `ml_ai_systems:model_drift_detected`).
- **MUST** use namespaces that correspond either to canonical module keys from `master_index.yaml.pattern_map` (for example, `security`, `domain.api_design`) or to org-qualified module keys that follow the module-key policy in RFC‑0001 Section 6 (for example, `org.foo.security`). These namespaces themselves act as module keys for the purposes of trigger and pattern resolution.
- **MUST NOT** redefine the meaning of a core trigger via a namespaced variant; extensions refine behavior, they do not contradict core semantics.

Core triggers in `FITPAC/docs/reference/trigger-taxonomy.md` are part of the normative surface pinned by the manifest described in RFC‑0001 Section 5. Adding new core triggers is a backward-compatible change (minor or patch); renaming or removing existing core triggers is a breaking change and **MUST** be accompanied by a major version bump of the relevant component and an updated manifest entry.

Project-local or experimental triggers **MAY** be used, but they **SHOULD** either:

- be mapped to existing taxonomy entries, or
- be clearly marked as experimental and avoided in long-lived specs. To reduce collisions between organizational packs, non-core triggers SHOULD use org-qualified namespaces (for example, `org.foo.*`) consistent with the module key naming scheme.

---

## 5. Parsing and Fragment-on-Demand Loading

For fragment-on-demand loading (as required by RFC-0001 and RFC-0004), implementations:

- **MUST** parse pattern files according to the structure in `pattern-index.md`:
  - identify `## pN` rule boundaries,
  - parse YAML blocks as valid mappings with required fields,
  - treat all content between rule headings as the rule body.
- **MUST** be able to load a pattern fragment by fragment ID (`<module>.pN`) without loading the entire module file into agent context.

Derived indexes (for example, trigger → `id` maps, embeddings, sharded stores) are **non-normative** and:

- **MUST NOT** change fragment IDs, module keys, or invariant identifiers.
- **MUST** be rebuildable from the normative surface (pattern files plus master index) alone.

---

## 6. Primitive Spine Exception

The file `FITPAC/00_primitive_spine.md` is the **primitive spine** (reference document, not a pattern module):

- It defines the canonical primitives and structural primitives.
- It lives outside `FITPAC/patterns/` and has **no** numbered rules `pN`; it has **no fragment IDs** of the form `<module>.pN`.

All rule-numbering requirements in this RFC and `pattern-index.md` apply to pattern modules under `FITPAC/patterns/` only.

---

## 7. Adding New Modules and Rules

When extending the pattern library, implementers:

- **MUST**:
  - choose a stable module key,
  - add it to `master_index.yaml.pattern_map`,
  - add rules with sequential `pN` numbering and complete metadata.
- **SHOULD**:
  - wire any new ambiguity triggers into `master_index.yaml.ambiguity_triggers`,
  - register new namespaced triggers in the corresponding pattern file and (if appropriate) `trigger-taxonomy.md`.

Existing module keys and fragment IDs **MUST NOT** be renamed or renumbered. Deprecated behavior is handled by:

- documentation, and/or
- new, higher-precedence rules or modules.

---

## 8. Normative References

The following files are normative references for this RFC:

- `FITPAC/docs/reference/pattern-index.md` — pattern format and parsing rules.
- `FITPAC/docs/reference/trigger-taxonomy.md` — trigger and condition taxonomy.
- `FITPAC/master_index.yaml` — canonical module keys and pattern map.
- `FITPAC/patterns/*.md` — pattern modules.

Distributions that relocate these files **MUST** provide equivalent artifacts and maintain the semantics described here to remain FITPAC-conformant. For FITPAC 1.0.0, the normative versions of these artifacts are those identified by the version-locking mechanism described in RFC-0001 Section 5 (for example, in `fitpac_manifest.yaml`).

