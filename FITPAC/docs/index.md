# FITPAC Pattern Language and Protocol

**FITPAC** (Formal Intent Translation Protocol for Agentic Code) is the **intent layer standard** for agent-native development. It combines:

- An **ontology** (primitives + patterns) that can describe everything a program does.
- A **protocol** (spec schema + master index) that tells agents when and how to consult that ontology and how to report what they did.

Use this `docs/` directory as the entry point for engineers who want to implement or evaluate **FITPAC‑conformant** agents. (Implementations are **conformant**; **FITPAC‑compliant** is the special case for Profiles only—see RFC-0001 §1.1 and RFC-0002.)

At a high level, FITPAC documentation is organized into:

- **RFCs (normative)** — Standards documents under `rfcs/` (RFC-0001 through RFC-0005 for core FITPAC 1.0.0, plus **RFC-0006** for the optional `fitpac.prose_compiler` extension) that define conformance, protocol behavior, primitives, spec schema, master index semantics, and pattern/trigger grammar.
- **Normative references** — Specific files that RFCs say implementations **MUST follow**, such as `FITPAC/master_index.yaml`, `FITPAC/00_primitive_spine.md`, and selected `FITPAC/docs/reference/*.md` pages. These documents declare `status: normative-reference` (or similar) in front-matter and may include an `implements: RFC-XXXX` field.
- **Informative docs and guides** — This `docs/` tree (guides, overviews, manifesto, getting-started). These documents explain how to use FITPAC and may restate RFC requirements but do not themselves add new conformance rules.

## Core ideas

- **Pattern language as intermediate layer:** Prose is not fed directly to code generators. It is first translated into a structured spec; that spec drives code generation and validation.
- **Consultation protocol:** Coding agents load `master_index.yaml` and, when confidence drops or a trigger fires, load only the listed pattern fragments; they apply the pattern and re-evaluate. Precedence (1 = highest) resolves conflicts.
- **Intent engineering:** FITPAC aligns with **intent engineering**—making organizational intent machine-readable and actionable (goal translation, decision boundaries, escalation, feedback). See [Intent engineering and industry alignment](reference/industry-alignment.md).

## Where to start

- **Integrators and product teams**
  - **Getting started:** [Getting started](getting-started.md) — Setup, first run, and where to find the run report and comparison report.
  - **Manifesto:** [FITPAC Manifesto](manifesto.md) — Intent engineering philosophy and why the protocol exists.
- **Standards and implementers**
  - **Big picture:** [Overview](overview.md) — Purpose, language vs protocol, fragment-loading discipline.
  - **Spec schema:** [Spec schema](reference/spec-schema.md) — Logical structure of specs (entities, invariants, boundaries, goals, etc.).
  - **Rules of the Road:** [Master index reference](reference/master-index.md) — Precedence, drop conditions, ambiguity triggers, consultation protocol.
  - **Pattern ontology:** [Pattern languages](patterns/index.md) — List of all pattern modules; see also `00_primitive_spine.md` for the 7 primitives and structural primitives.
  - **Extension registry:** [Extension registry](reference/extension-registry.md) — Registered additive packs (reference distribution: `fitpac.prose_compiler`).
  - **Guides:**
    - [Prose to spec](guides/prose-to-spec.md) — Retrieval flow and Socratic behavior.
    - [Spec to code](guides/spec-to-code.md) — When to consult, what to load, consultation procedure.
  - **Prose→primitives (extension):** [`fitpac.prose_compiler` pack](../extensions/fitpac_prose_compiler/) — Compiler pipeline, schemas, and [`prose-to-primitives runbook`](../extensions/fitpac_prose_compiler/docs/guides/prose-to-primitives-pipeline.md); resolve paths with `python3 FITPAC/tools/fitpac_prose_compiler_context.py`.
