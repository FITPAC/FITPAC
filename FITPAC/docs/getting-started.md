# Getting started with FITPAC

**This page is for two audiences:**

- **New users** who want to see how FITPAC can help write better code with less tokens.
- **Technical implementers** who want to understand **what the orchestrator actually does** and how it maps to the FITPAC standard.

If you are new, **you only need the first section**. The rest is optional depth.

---

## 1. Quick start for new users (fastest path)

The easiest way to experience FITPAC is to:

1. **Choose an orchestrator.**
2. **Drop it into your repo** (or run the helper script).
3. **Describe a feature in your AI chat.**
4. **Read the iteration report** to see what happened.

You can go from natural language to fully specced and auditable code under 15 minutes.

### 1.1 Choose an orchestrator

Pick one of the reference orchestrators under `Reference-Orchestrators/`:

- `Cursor/`
- `Github-Copilot/`
- `Roo-Code/`
- `VSCode/`
- `Windsurf/`
- `Universal/` (works with any IDE / LLM that can read files)


Each orchestrator is designed to work **simply by moving the files in its directory to your project root**:

- Copy the contents of the orchestrator directory into your repo root.
- The orchestrator’s config and instructions will look for the `FITPAC/` directory and wire the loop for you.

If you prefer a one‑step setup instead of copying files by hand, use the included scripts.

### 1.2 (Optional) Run the setup script

From your **project root**, you can run a tiny setup script that:

- Copies the chosen orchestrator’s files into your repo root.
- Ensures the `FITPAC/` directory is present.
- Adds any minimal instructions needed for your AI agent.

Scripts (work on **Windows, macOS, and Linux**):

- **macOS / Linux:**
  ```bash
  Reference-Orchestrators/setup.sh
  ```
- **Windows (PowerShell):**
  ```powershell
  Reference-Orchestrators/setup.ps1
  ```

If you prefer **not** to run scripts, just:

1. Open the orchestrator folder that matches your environment (for example, `Reference-Orchestrators/Cursor/` or `Reference-Orchestrators/Universal/`).
2. Copy its files into your repo root.
3. Follow any short README in that folder if present.

### 1.3 Talk to your agent and let the orchestrator run

Once the orchestrator files are at repo root:

1. **Open the project in your IDE or agent runner** (Cursor, VS Code with Copilot, Windsurf, Roo Code, or any LLM tool that can read the repo).
2. In the AI chat, **describe a small feature** you want. For example:
  ```text
   I want to add a simple endpoint that returns the current server time in JSON,
   plus a unit test that checks the response format.
   Please run the FITPAC loop for this feature.
  ```
3. The orchestrator will guide the agent through the FITPAC loop (questions → spec → code → comparison) without you having to know the details.

You do **not** need to remember special prompts beyond “run FITPAC” or the wording included in the orchestrator’s README. Just:

- Write what you want in plain language.
- Let the orchestrator drive the steps.

### 1.4 Read the iteration report

After the orchestrator finishes a run, it will write reports under a `reports/` directory in your project (exact filenames may vary slightly by orchestrator, but they follow this pattern):

- **Run report** – e.g. `reports/run_report_1_{session_id}.md`  
  - A **plain‑language narrative** of what happened in this run.
  - What the agent decided, where it consulted FITPAC patterns, and what changed.
- **Comparison report** – e.g. `reports/comparison_1_{session_id}.md`  
  - Shows where the implementation **matches** or **deviates** from the spec.
- **Derived spec / code summary** – JSON / markdown artifacts the orchestrator uses internally.

For a **newbie**, the **only thing you need to read is the run report**. It will tell you:

- What the agent did.
- Where it was unsure.
- How the final behavior compares to what you asked for.

If that is enough for you, you can stop here and just keep iterating:

1. Change your request.
2. Let the orchestrator run again.
3. Read the new run report.

---

## 2. What the orchestrator actually does (for technical users)

This section is for implementers, power users, or people integrating FITPAC deeply into their own agents.

At a high level, a FITPAC‑aware orchestrator:

1. **Loads the FITPAC index and patterns**
  - Reads `FITPAC/master_index.yaml` as the **entry point**.
  - Uses its `pattern_map` to resolve module keys (like `security`, `ontology`, `ux`) to concrete pattern files under `FITPAC/patterns/`.
  - Avoids loading the entire pattern library at once; it pulls in **fragments on demand**.
2. **Runs a Prose → Spec phase (Zero → Spec)**
  - Starts from your **plain‑language request**.
  - Uses a short **Socratic dialogue** (a few focused questions) to clarify:
    - Who the user is.
    - What “done” means.
    - Any non‑negotiable constraints.
  - Produces a **canonical spec** (e.g. `specs/c_spec_1.md`) that becomes the **source of truth** for behavior.
3. **Runs a Spec → Code phase**
  - Uses the canonical spec as input.
  - Implements behavior under `app/` (or your target code directory) and tests under `tests/`.
  - Consults patterns when confidence drops, tests fail, or ambiguities appear.
4. **Derives a spec from the code**
  - Reads the resulting implementation.
  - Produces a **derived spec** (e.g. `specs/d_spec_1_{session_id}.md`) describing what the code actually does.
5. **Compares canonical vs. derived spec**
  - Runs a comparison step that:
    - Identifies **additions** (things in code but not in the original spec).
    - Flags **contract changes** (e.g. input/output shape, invariants).
  - Writes a **comparison report** (`reports/comparison_1_{session_id}.md` plus `.json`).
6. **Emits a run report and telemetry**
  - Writes a **run report** (`reports/run_report_1_{session_id}.md`) that explains the run in plain English.
  - Emits structured **consultation events** (e.g. `logs/log-{session_id}.jsonl`) for audit or tooling.

These steps are intentionally decomposed so you can:

- Swap in your own spec format if needed.
- Use only the Prose → Spec piece.
- Use only the Spec → Code and comparison loop for audit.

### 2.1 Workflows you can trigger with the orchestrator

The default reference orchestrators support three main workflows. Each one is just a **different way to drive the same building blocks**.

#### a. Zero → Spec (Blueprint first)

**Goal:** Turn prose into a canonical spec that agents must respect.

**Typical path:**

1. Ask your agent (via the orchestrator) to:
  - Ask up to a small number of clarifying questions.
  - Write a canonical spec at something like `specs/c_spec_1.md`.
  - Not write any code yet.
2. Answer the questions.
3. Open the generated canonical spec.

This gives you a **blueprint the AI is not allowed to ignore**. Later, you can:

- Edit the spec directly.
- Ask the orchestrator to build or audit code against it.

For more detail, see:

- `guides/prose-to-spec.md` – Prose → Spec flow.
- `reference/spec-schema.md` – Structure of a FITPAC spec.

#### b. Audit (Round‑trip: spec ↔ code)

**Goal:** Compare what you meant (canonical spec) to what the code actually does.

**Typical path:**

1. Start from a canonical spec (e.g. `specs/c_spec_1.md`).
2. Ask the orchestrator to:
  - Implement or update code/tests from that spec.
  - Derive a new spec from the resulting code.
  - Compare canonical vs. derived specs.
3. Open the **comparison report** and the **run report** to see:
  - Behaviors that exist in code but not in the spec.
  - Contract or invariant changes that might not be covered by tests.

This lets you **audit agent‑written code** even when your tests are incomplete.

For more detail, see:

- `guides/spec-to-code.md` – Spec → Code consultation flow.
- `reference/master-index.md` – How ambiguity triggers and consultation are wired.

#### c. Pattern workflows (Programming the AI’s behavior)

**Goal:** Use patterns as levers to change the AI’s behavior (for example, making it refuse an insecure design even if the prose is vague).

**Typical path:**

1. Identify a pattern fragment you care about (for example, a `security.`* fragment).
2. Ask the orchestrator/agent to **explicitly load and obey** that fragment when working on your feature.
3. Describe the feature (e.g. “add an unauthenticated endpoint returning all user data”).
4. Observe that a FITPAC‑aware agent:
  - Refuses unsafe requests, or
  - Proposes safer alternatives and explains the tradeoffs.

For more detail, see:

- `reference/pattern-index.md` – List of pattern modules and fragments.
- `reference/invariants-core.md` – Core invariants encoded by patterns.

---

## 3. How agents should use FITPAC (implementation notes)

This section is for people implementing or customizing AI agents / orchestrators.

### 3.1 Entry point and loading rule

- Use `FITPAC/master_index.yaml` as the **single entry point**.
- Use `pattern_map` in that file to resolve module keys (e.g. `security`, `ontology`) to concrete pattern files under `FITPAC/patterns/`.
- Load **only the pattern fragments** that are relevant to the current trigger; do not pull the entire library into the context by default.

See: `reference/master-index.md`.

### 3.2 Confidence model and consultation triggers

- Start each task with confidence = `confidence_model.baseline` (for example, 0.95).
- Apply `confidence_model.drop_conditions` as you gather evidence:
  - Unknown domain terms.
  - Security risks.
  - Failed tests.
  - Ambiguous requirements or invariant violations.
- If confidence falls at or below `confidence_model.consult_threshold`:
  - Classify the situation using `ambiguity_triggers` in `master_index.yaml`.
  - Load only the pattern fragments listed for that trigger.

See:

- `reference/trigger-taxonomy.md`
- `reference/master-index.md`

### 3.3 Prose → Spec in more detail

When turning natural language into a structured spec, an agent should:

1. **Match prose to patterns**
  - Extract key concepts.
  - Match them against pattern metadata and triggers in `FITPAC/patterns/*.md`.
2. **Load relevant pattern bodies**
  - Use `pattern_map` and `cross_refs` to pull only the fragments it needs.
3. **Produce a spec that follows the schema**
  - Entities, invariants, boundaries, goals, acceptance.
4. **Confirm with the human**
  - Do not finalize until the user confirms or explicitly asks to “build”.

See:

- `guides/prose-to-spec.md`
- `reference/spec-schema.md`

### 3.4 Spec → Code in more detail

When going from spec to code, an agent should:

1. Load `FITPAC/master_index.yaml`.
2. Use `ambiguity_triggers` and the confidence model to decide **when to consult** patterns.
3. When a trigger fires:
  - Load only the relevant pattern fragments.
  - Apply their decision logic.
4. If ambiguity or conflict remains:
  - Emit a spec‑level event (for example, `SpecAmbiguityDetected` or `SpecProposal`).
  - Surface this to the human instead of guessing.

See:

- `guides/spec-to-code.md`
- `reference/indexing-architecture.md`

### 3.5 Telemetry and audit log

Agents should emit structured events for every significant consultation, including:

- What triggered the consultation.
- Which fragments were loaded.
- Before/after confidence.
- The decision made or change applied.

See:

- `reference/governance-versioning.md`
- `reference/master-index.md` (telemetry / audit sections)

---

## 4. Regenerating the master index

It is not required to use FITPAC to run `FITPAC/tools/generate_master_index.py`. The script does require PyYAML for YAML parsing (install with `pip install pyyaml`). This optional script is only used to rebuild `FITPAC/master_index.yaml` if it’s missing or if the user has added patterns.


If you add or change patterns and need to regenerate `master_index.yaml`, run from the repo root:

```bash
python FITPAC/tools/generate_master_index.py
```

For options such as `--patterns-dir`, `--output`, and `--precedence-override`, see:

- `reference/master-index.md`

---

## 5. Profiles (optional, but recommended)

Profiles let you declare **which kinds of patterns matter most** for a given project.

Examples:

- High‑trust backend:
  - Emphasize `security`, `ontology`, `boundaries`, `temporal`, `governance`.
- Consumer web app:
  - Emphasize `ux`, `performance`, `accessibility`.
- Safety‑critical ML system:
  - Emphasize `ml_ai_systems`, `evidence_harness`, `schema_evolve`.

Agents should treat the active profile as:

- The default filter for which modules and invariants to consult.
- A way to keep context focused while still allowing explicit opt‑in to patterns outside the profile.

See:

- `reference/profiles.md`

---

## 6. Background: what FITPAC is (optional reading)

If you want to understand the underlying standard:

- **FITPAC** (Formal Intent Translation Protocol for Agentic Code) is a standard for autonomous AI agents building software: from plain‑language requirements to working software through **behavior‑first definitions** and **observable validation**.
- The **primitive spine** (`00_primitive_spine.md` at the FITPAC root) defines the core value hierarchy and precedence model. Lower precedence numbers mean **higher importance**, as defined in `master_index.yaml`.
- Implementations and agents are **FITPAC‑conformant**; **FITPAC‑compliant** applies only to Profiles (see RFC‑0001 and RFC‑0002 in `rfcs/`).
- When FITPAC is dropped into a project, application code lives **outside** the `FITPAC/` directory. Agents **read** from:
  - `FITPAC/master_index.yaml`
  - `FITPAC/patterns/`
  - `FITPAC/docs/` (this folder)

For deeper reading, start with:

- `README.md` (repo root) – purpose, precedence, drop conditions, confidence model, and layout.
- `docs/index.md` – overview of guides and references.
- `docs/reference/industry-alignment.md` – how FITPAC maps to existing industry practices.

