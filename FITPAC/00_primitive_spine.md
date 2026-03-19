# Primitive Spine (Reference)
# Version: 1.0.0
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Copyright Holder: Paul Roy and FITPAC Contributors
# Attribution Note: Attribution required under CC BY 4.0.

This document defines the canonical primitive set for the FITPAC pattern language. All patterns map to these primitives. It is the single reference for Layer 1 (core) and Layer 2 (structural) primitives and for current aliases used in pattern prose.

The pattern language functions as the intermediate layer between human prose and machine-readable structured spec.

---

## Normative contract

- **Single computation model:** Every FITPAC pattern **must be expressible as a composition of these primitives only** (Layer 1 and Layer 2), plus ordinary data types. Pattern modules MAY introduce *names* and *shortcuts* for common compositions, but they MUST NOT introduce new, incompatible models of computation.
- **No hidden semantics:** Domain modules (e.g. `messaging`, `ml_ai_systems`, `accessibility`) may *constrain*, *combine*, or *specialize* primitives, but they do not change the core execution or constraint‑evaluation semantics defined here.
- **Compositional safety:** When a pattern refers to a domain concept (e.g. "async command queue", "approval workflow"), that concept MUST be explainable as:
  - a set of Entities and Transformations,
  - governed by Constraints and Policies,
  - flowing across Boundaries and Transactions,
  - under Authorities, Relations, Context, and Time.

This contract is what makes it possible for:

- the **spec schema** to stay stable across domains and implementations, and
- new pattern modules to be added without altering the underlying meaning of existing specs.

---

## Layer 1: Core primitives

| Primitive      | Short definition |
|----------------|------------------|
| **Entity**     | A thing that can be identified and may have state; the unit of storage and identity. |
| **Transformation** | A change of state or a recorded occurrence; the unit of "what happened" or "what will happen." Each transformation has an execution semantics (how it is applied) that may be declared or implied. |
| **Constraint** | A rule that must hold (invariant, legality condition, or validation rule). Each constraint has an evaluation semantics (when it is checked, failure mode) that may be declared or implied. |
| **Authority**  | Who or what is allowed to perform an action; the unit of "who may do what." |
| **Relation**   | A link between entities or between entities and authorities (ownership, association). |
| **Context**    | Ambient or request-scoped information that affects interpretation (locale, tenant, trace). |
| **Time**       | Ordering, duration, deadlines, and time sources; the unit of "when" and "how long." |

- **Stability (normative):** This Layer 1 primitive set is **sacrosanct** and **MUST NOT** be redefined or extended by profiles, pattern modules, or implementations. Domain modules MAY specialize or constrain these primitives but do not introduce new core primitives.

---

## Layer 2: Structural primitives

| Primitive      | Mapping from core | Short definition |
|----------------|-------------------|------------------|
| **Transaction**| Boundary around a set of transformations that commit or roll back together. | Atomic unit of work. |
| **Boundary**   | Interface between contexts (service, process, trust zone); owns contract and error taxonomy. | Cross-boundary interaction and contracts. |
| **Projection** | Derived view from entities/transformations (read model, snapshot). | Materialized or computed view. |
| **Capability** | Subset of Authority; minted, scoped, and revocable. | Delegatable permission. |
| **Policy**     | Structured Constraint (e.g. access rule, approval tier). | Decision rule or policy artifact. |

- **Extensibility (normative):** Structural primitives MAY be extended by domain modules with additional compositions, provided they remain consistent with the core semantics above and with RFC‑0001 (FITPAC 1.0.0). Extensions MUST NOT alter execution or constraint‑evaluation semantics of the underlying Layer 1 primitives.

---

## Core semantics

The language describes not only *what* exists and *what* can change, but *how* change is interpreted and enforced. This is **core semantics**; domain modules do not redefine it.

- **Execution semantics:** How a Transformation is interpreted/executed (the model of computation). Examples: state-machine transition, function application, event append + projection, saga step, actor message processing. When unspecified, left to implementation or pattern.
- **Constraint evaluation semantics:** When constraints are checked (e.g. before commit, after, continuously) and how violation is handled (reject, compensate, escalate). Domain patterns (e.g. ontology p9) may specify "check before commit; failure = RejectEvent"; the spine defines that such timing and failure mode are the evaluation semantics of constraints.

---

## Current alias (keep in pattern prose)

Existing patterns may continue to use these names. They map as follows:

| Alias     | Primitive       | Notes |
|-----------|-----------------|--------|
| **Actor** | Authority      | The "who" in policy checks and delegation. |
| **Resource** | Entity      | The "what" being stored, read, or mutated. |
| **Event** | Transformation  | A record of something that happened (or a command to be applied). |
| **Capability** | Authority (modifier) | Already in Layer 2; minted, scoped permission. |
| **Policy** | Constraint   | Already in Layer 2; structured constraint. |

No refactor is required to rename Actor → Authority or Resource → Entity everywhere; a single "Maps to: Entity, Authority" (or equivalent) per pattern is enough.

---

## Domain rule

- **Domain primitives** (e.g. in [messaging.md](patterns/messaging.md), [ml_ai_systems.md](patterns/ml_ai_systems.md), [accessibility.md](patterns/accessibility.md)) must be **documented as compositions of core/structural only** and **namespaced** (e.g. `messaging`, `ml_ai`, `a11y`).
- Domain modules do not redefine core semantics; they add constraints, type aliases, or domain-specific invariants built from Entity, Transformation, Constraint, Authority, Relation, Context, Time, Transaction, Boundary, Projection, Capability, Policy.

---

## Retrieval and index

Implementations may derive a machine-readable index from the pattern files. Each pattern declares `requires_primitives`, `produces`, `output_type`, and `triggers`; the spine is the reference for naming those primitives consistently. The **normative pattern format** (required/optional YAML fields, categories, and sequential numbering of rules) is defined in [docs/reference/pattern-index.md](docs/reference/pattern-index.md).
