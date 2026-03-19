### FITPAC: Formal Intent Translation Protocol for Agentic Code

**FITPAC** translates human intent into a machine-optimized structured software specification. It reduces ambiguity and creates an auditable trail between what software designers envision and what the code actually does.

The protocol governs the entire lifecycle of a codebase: it helps engineers write the spec, guides the coding agent to write the code, enables a decoding agent to reverse-engineer a derived spec, and ultimately ensures the engineers knows for sure that the code contains everything specified—and nothing else.

**New to FITPAC?** **[Getting started](FITPAC/docs/getting-started.md)** walks you through setup and your first run. After each run you get a **run report** (plain-language summary) and a **comparison report** (spec vs. code) in `reports/`, each with a timestamped suffix.

---

### 🌐 Industry Context: Intent Engineering

We are moving beyond the era of **Prompt Engineering** (choosing words carefully to coax desired behavior) and **Context Engineering** (providing agents with the specific data needed to perform a task).

FITPAC represents the shift toward **Intent Engineering**. It is a formal framework that translates what you *mean* into code that works exactly as you *expect* it to. By defining a shared ontology and a rigorous consultation protocol, FITPAC ensures that organizational intent is machine-readable, enforceable, and persistent across different agent stacks.


| Approach            | What you do                                            |
| ------------------- | ------------------------------------------------------ |
| Prompt Engineering  | Coax behavior with carefully worded prompts            |
| Context Engineering | Feed the model the right documents and data            |
| Intent Engineering  | Formalize what you mean into executable specs (FITPAC) |


---

### 💡 Key Benefits

#### Iterate the Prompt, Not the Code

FITPAC allows you to resolve ambiguity and enforce non-negotiable constraints before an agent writes a single line of code. By shifting the iterative cycle to the structured specification layer, you avoid the "drift" and technical debt associated with repeated, unguided code generations.

#### Audit Agent Work: Canonical vs. Derived

FITPAC enables a unique "round-trip" audit capability.

- **Canonical Spec:** The original intent-based specification, written by a human and translated into a structured machine-optimized format using the FITPAC protocol.
- **Derived Spec:** A specification reverse-engineered from the resulting code by an agent that understands the FITPAC control grammar but has no access to the original spec.

By comparing the two, you can verify if the implementation aligns with the intent.  This process can be fully automated via an orchestration layer.  Multiple reference orchestrators are included with the repo so you can get started quickly in your IDE of choice.

#### Peek into the Black Box

Whenever the agent reaches an inflection point and is unsure how to proceed due to spec ambiguity or multiple valid implementation paths, it emits a log event in plain English explaining why it paused, what pattern it picked, and how confident it was to proceed.

#### Lightweight Pattern Language

FITPAC’s pattern language is intentionally lightweight (17.4 Kilobytes).  Pattern snippets are loaded on demand and are very small, so the agent’s context window stays lean. A tiny set of rules allows agents to solve common coding challenges in unlimited ways while retaining compliance to spec and enabling a full audit trail.

#### Works with All Programming Languages

The primitives and control grammar are language-agnostic and expressed in plain English, so FITPAC is compatible with any programming language. Most users will be working in Rust, Python, C, or similar; those using Assembly, LISP, or other specialized languages may need to write patterns specific to their use case.  Full documentation is provided for this purpose.

#### Expandable and Customizable

Write your own patterns to solve specific coding challenges or define organizational intent. Customize your own hierarchy of importance (e.g., Security is more important than UI) to fit your domain needs.  FITPAC comes with 30 pattern modules by default (plus the primitive spine reference at `FITPAC/00_primitive_spine.md`), with the ability to expand to any arbitrary number of specialized patterns via namespacing.  Built in dot versioning for the ontological primitives, control grammar, and patterns ensures code compatibility even if the language is updated mid project.

---

### 🚀 Quick Start (pick your track)

There are two ways to approach this repo:

- **I just want to try it (≈5 minutes)**  
  - **Step 1:** From your project root, run:  
    - Unix (macOS/Linux): `Reference-Orchestrators/setup.sh`  
    - Windows: `Reference-Orchestrators/setup.ps1`
  - **Step 2:** Open the project in your IDE (Cursor, VS Code + Copilot, Windsurf, Roo Code, etc.).  
  - **Step 3:** In your AI chat, describe a small feature and ask it to **“run the minimal FITPAC loop”**.  
    - When it finishes, open:
      - `specs/c_spec_1.md` (your canonical spec)  
      - `reports/run_report_1_*.md` (what happened)  
      - `reports/comparison_1_*.md` (spec vs code)
  - **Outcome:** You see FITPAC’s **Zero → Spec** and **Audit** workflows end‑to‑end without touching any config.
  - **If the setup script fails or you prefer not to run it:** open the appropriate README under `Reference-Orchestrators/` (for example, the **Universal** or your IDE-specific package) and copy the provided “universal instructions” into your IDE’s **System Prompt** or **Custom Instructions**. This gives you a FITPAC-aware minimal loop without running any scripts.
- **I want to implement the standard**  
  - Read **[Getting started](FITPAC/docs/getting-started.md)** (Toolbox‑style guide with:
    - Zero → Spec,
    - Audit,
    - Pattern workflows).
  - Then, for protocol details and conformance:
    - RFCs under `rfcs/` (normative standard), and  
    - `FITPAC/docs/reference/*.md` (spec schema, master index, pattern index, trigger taxonomy, governance, profiles).

Everything in this repo is drag‑and‑drop: you can copy the `FITPAC/` directory and reference orchestrator files directly into an existing project.

---

### 🧩 Use Cases

- **Dark Factories and Agent Platforms**  
Prompts → Canonical specs → code; every consultation logged for governance. FITPAC can be implemented into any dark factory loop using plain English agent instructions, detailed in the Docs.
- **Regulated and Safety-Critical Environments**  
Security, privacy, invariants, and approval flows as explicit patterns and specs; value hierarchy and drop conditions enforce non-negotiable constraints.
- **Internal Platforms and Monolith Rewrites**  
Behavior defined in specs first; code treated as an implementation detail that can be regenerated.
- **Cross-Vendor Interoperability**  
Different agent stacks (Cursor, Replit, internal tools, etc.) use the same primitives, spec schema, consultation protocol, and audit semantics.
- **Alignment and Continuous Improvement**  
Canonical vs Derived specs plus the audit log show how code diverges from intent and tighten both specs and patterns.

---

### ✅ FITPAC Compliance and Documentation Authority

RFCs are the **normative standards documents** for FITPAC; they may designate additional files as **normative references** (for example, `FITPAC/00_primitive_spine.md`, `FITPAC/master_index.yaml`, and selected `FITPAC/docs/reference/*.md` files).

Informally:

- **FITPAC-conformant**  
An agent or platform is FITPAC-conformant when it:
  - Uses `FITPAC/master_index.yaml` as the unified context entry point (pattern map, precedence, confidence model, ambiguity triggers, consultation protocol).
  - Implements the **ambiguity protocol**: confidence model with baseline/consult threshold, deterministic condition-to-fragment mapping, minimal fragment loading, escalation when unresolved, and an audit log with human-readable reasoning.
  - Works over **FITPAC specs** (Canonical and Derived) that follow the spec schema and control grammar (REQUIRE, RULE, EMIT, NOTE), and performs round-trip comparison including an **Additions (not in spec)** section and classification of differences as cosmetic, behavioral, or contractual.
  - Preserves **stable identifiers** for modules and fragments (`<module>.pN`) and uses the module keys from `FITPAC/master_index.yaml.pattern_map` as the canonical IDs.
  - Resolves conflicts using a deterministic, documented **value hierarchy** (precedence_hierarchy).
  - Emits **auditable consultation events** with plain-English reasoning for every consultation, using the event structure defined in `FITPAC/master_index.yaml`.
- **FITPAC-conformant (Standard Profile)**  
In addition to the above, an implementation is FITPAC-conformant (Standard Profile) when its precedence hierarchy satisfies the Standard FITPAC Profile principle: constraints protecting safety, integrity, and regulatory compliance outrank those optimizing only for convenience, performance, or resource budgets.
- **Profiles and experiments**  
Implementations that support Profiles MUST load only FITPAC-compliant profiles as defined in RFC-0002 (profiles tighten; they do not loosen) and SHOULD clearly label any experimental or non-standard profiles in their audit logs.

For human readers, the `FITPAC/docs/` tree (especially `FITPAC/docs/getting-started.md` and `FITPAC/docs/guides/`) serves as the **user and implementer manual**. Unless a document in that tree is explicitly marked as a normative reference implementing a particular RFC, it should be treated as **informative**: it explains how to use FITPAC but does not, by itself, introduce new conformance requirements.

---

*FITPAC is an open standard for the era of agentic software engineering.*

---

## License

This repository is licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). See `LICENSE` for the full license text.