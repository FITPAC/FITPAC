---
title: Spec schema (Canonical and Derived specs)
status: normative-reference
implements: RFC-0003
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
copyright_holder: Paul Roy and FITPAC Contributors
attribution_note: Attribution required under CC BY 4.0.
---

# Spec schema (Canonical and Derived specs)

For **pre-spec vs post-spec comparison** to be deterministic, both the Socratic output and the reverse-spec (code → spec) must use the **same schema**. FITPAC calls these the **Canonical** and **Derived** specs.

This document describes that schema at a level suitable for implementors; the exact representation (Markdown sections, YAML frontmatter, or another structured form) is left to each implementation.

## 1. Foundations

The spec schema is defined by:

- **Primitives** — See `00_primitive_spine.md`:
  - Layer 1: Entity, Transformation, Constraint, Authority, Relation, Context, Time.
  - Layer 2: Transaction, Boundary, Projection, Capability, Policy.
  - Aliases: Actor, Resource, Event.
- **Pattern modules** — Especially:
  - `patterns/domain_ontology.md` — entities, mappings, state legality, invariants.
  - `patterns/boundary_contracts.md` — boundaries, error taxonomy, retry budget.
  - `patterns/satisfaction_goals.md` — goals, acceptance, satisfaction rubric.
  - `patterns/security_trust.md`, `patterns/governance.md`, `patterns/evidence_harness.md`, etc.

The spec schema is **how these primitives and patterns are serialized** into a single document that agents can produce, consume, and compare.

## 2. Naming and lifecycle (conceptual)

- **Canonical** — A spec produced from human input (prose → structured spec).
- **Derived** — A spec extracted from code (spec → code → spec).

Implementations may pair them by index (e.g. Canonical_1 vs Derived_1) for comparison. FITPAC does not define where or how specs are stored; that is defined by your orchestration or workflow layer.

## 3. Logical sections (canonical schema)

A FITPAC spec is logically divided into sections. Implementations may choose their own exact headings, but the **content** should cover:

1. **Entities and ontology**
   - Core entities and resources.
   - Ontology mappings and state diagrams.
   - Links to invariants and boundaries.
2. **Constraints and invariants**
   - Global invariants and per-entity constraints.
   - Legality rules for state transitions.
   - Optional references to named invariants (e.g. `api_design.inv.1`, `privacy_data_protection.inv.4`) where the pattern library or project has chosen to expose stable IDs. Use the **module key** from `pattern_map` (see [pattern-index.md](pattern-index.md)).
3. **Authorities and policies**
   - Actors and roles.
   - Capability and delegation rules.
   - Governance and approval requirements.
4. **Boundaries and transactions**
   - External and internal boundaries (APIs, queues, DBs, services).
   - Transaction boundaries, retry budgets, idempotency semantics.
5. **Temporal behavior**
   - Deadlines, leases, retries, time sources.
   - Concurrency model and ordering guarantees.
6. **Goals and acceptance**
   - Satisfaction goals and target outcomes.
   - Acceptance criteria and scoring/rubrics.
7. **Evidence and scenarios**
   - Key scenarios and test cases.
   - Properties and falsification strategies.
8. **Design summary (optional)**
   - Plain-language summary of the design and trade-offs.
   - Used by coding agents only when resolving ambiguity.
   - For specs produced by the Socratic (prose→spec) flow, this summary typically includes the conversation context (intents, clarifications, decisions) that led to the spec.

Only sections 1–7 are treated as **structured content** for comparison. The design summary is intentionally excluded from structural diffs.

## 4. Pre-spec vs post-spec

- **Pre-spec (Canonical_N)** — Output of the Socratic LLM (from prose).
  - MUST use the schema above to describe primitives, constraints/invariants, boundaries, authorities, goals, and evidence.
  - MAY refer to invariants by stable IDs using the **module key** (e.g. `api_design.inv.1`) where such IDs exist, or by spec-local names when no stable ID is available.
- **Post-spec (Derived_M)** — Extracted from the generated code using the **same schema** (same sections, same underlying primitives and patterns).
  - Implementations perform **extraction only** in this step; comparison is separate.
  - Extractors MAY attach invariant identifiers that were inferred from code patterns (e.g. linking a check back to `api_design.inv.1`) but are not required to rely on a central invariant registry; they can instead map directly to patterns or spec-local constraint names.

## 5. Comparison and reports

When comparing Canonical and Derived specs:

- **Comparison target:** treat both specs as structured documents over the same schema (entities, constraints/invariants, boundaries, goals, etc.).
- **Comparison reports** MUST include:
  - Identifiers of the specs being compared (e.g. `Derived_2` vs `Canonical_1`).
  - An **Additions (not in spec)** section listing every element present in the Derived spec but not in the Canonical spec (id, location, description, suggested action). This section MUST appear even if empty (e.g. `None`).
  - Other differences, classified as **cosmetic**, **behavioral**, or **contractual** (e.g. signature changes, boundary shifts, invariant weakening/strengthening).
- **Diff mechanics:** implementations may compare normalized representations (YAML/JSON, key paths) or structured Markdown, but the semantics should follow the schema above. In particular:
  - where stable invariant IDs exist (e.g. `temporal.inv.1`), they provide a convenient anchor for diffs, but
  - comparison MUST NOT assume that all invariants have global IDs; specs MAY describe some constraints only in structured prose or spec-local identifiers.

Where comparison reports are produced and how they feed back into the coding loop is defined by your implementation. See [Scenarios and round-trip](../guides/scenarios-roundtrip.md) for an informative overview.

---

## 6. Control grammar (normative)

While the spec schema describes *what* must appear in Canonical/Derived specs, the **control grammar** describes *how pattern‑driven sections are structured* in Markdown. Implementations SHOULD treat this grammar as the single source of truth for section parsing.

### 6.1 Section vocabulary

**Spec documents** use a **closed set** of section labels for structured content:

- `REQUIRE` — Preconditions, invariants, and obligations (maps primarily to **Constraint** and **Policy** primitives).
- `RULE` — Operational rules and control flow (maps primarily to **Transformation**, **Boundary**, **Transaction**, and **Policy**).
- `EMIT` — Outputs, events, or artifacts produced when the rule fires (maps to **Transformation**, **Projection**, or externalized artifacts).
- `NOTE` — Non‑normative commentary and explanation (ignored by structural diffs).

Implementations MAY support additional headings for readability, but only these four sections are considered **control vocabulary** for execution and comparison semantics.

**Pattern rule bodies** in `patterns/*.md` may use these labels or express the same semantics in free-form prose and bullet lists; see [pattern-index.md](pattern-index.md) for the normative rule (existing content is compliant either way).

### 6.2 EBNF-style definition

At a high level, a pattern‑driven spec section can be described as:

```text
Spec              ::= Header? FrontMatter? Section+

Section           ::= RequireSection
                    | RuleSection
                    | EmitSection
                    | NoteSection

RequireSection    ::= "REQUIRE" Block
RuleSection       ::= "RULE" Block
EmitSection       ::= "EMIT" Block
NoteSection       ::= "NOTE" Block

Block             ::= Paragraph+
Paragraph         ::= Line+ (blank-line)
Line              ::= any-text-except-heading
```

Pattern files add YAML rule metadata (see `docs/reference/pattern-index.md`) on top of this grammar; spec documents MAY mirror that structure in frontmatter but are not required to.

### 6.3 Typed flow and composition

Patterns and specs compose over the primitives defined in `00_primitive_spine.md`:

- `requires_primitives` declares which primitives a rule *reads or constrains*.
- `output_type` declares the *kind of artifact* produced (constraint, decision, mapping, etc.).
- Optional `produces` gives a more concrete handle for the emitted artifact (e.g. `SpecAmbiguityDetected`, `WriteOwnerConstraint`).

Implementations SHOULD treat a rule as a **typed function**:

```text
requires_primitives × inputs  →  output_type (produces?)
```

Composition across rules follows these principles:

- Within a module, rules are ordered by their `pN` index; consuming agents MAY rely on this as a **stable, deterministic evaluation order** when the module does not specify something stronger.
- Cross‑module references occur only through explicit `cross_refs` and invariant identifiers (e.g. `ontology.inv.1`); implementations MUST NOT infer precedence from file names or headings alone.
- Derived indexes (e.g. "all rules that emit `SpecAmbiguityDetected`") operate purely on this typed surface (`id`, `triggers`, `requires_primitives`, `output_type`, `produces`, `domain`, `category`) and do not change semantics.

This control grammar, together with the primitive spine, ensures that all patterns and specs share one small, composable execution model even as the library grows.

---

In practice, the spec schema is the **contract** between:

- The **Specification Guide** (prose → Canonical specs),
- The **Coding agent** (Canonical specs → code),
- The **Code-to-Spec Guide** (code → Derived specs),
- And the **Spec Comparison Guide** (Canonical vs Derived).

Keeping this schema stable and well-defined is what makes FITPAC round-trip comparison and cross‑platform interoperability possible.
