# Prose to spec

This guide describes **prose → structured spec**: goal translation from human prose to an agent-actionable structured spec. It focuses on how to match user prose to patterns and how a Socratic LLM can produce a structured spec in the format defined by the [Spec schema](../reference/spec-schema.md). The **normative rules** for pattern metadata, trigger taxonomy, and retrieval live in RFC-0003, RFC-0005, and the reference docs under `FITPAC/docs/reference/`; this page is **informative** and presents a recommended workflow.

## Retrieval flow

One practical retrieval strategy for prose → spec is:

1. **Extract features/keywords** from user prose (or use embeddings) and map them to pattern `triggers`, `domain`, and `category` in `patterns/*.md`.
2. **Match** against pattern metadata to obtain a candidate list of pattern IDs whose `triggers` match.
3. **Sort matched patterns by category** as a retrieval heuristic (for example: security → invariant → ownership → domain → boundary → other) so that safety‑critical and invariant rules are considered early. This is only a local heuristic; the global value hierarchy is encoded separately in `precedence_hierarchy` in `FITPAC/master_index.yaml`.
4. **Load** only the corresponding pattern bodies from `patterns/*.md` (or from a cache keyed by pattern id), rather than scanning the entire library.
5. **Resolve `cross_refs`** lazily: if a loaded pattern references another fragment (for example, `security.p3`), load that pattern as needed.
6. **Inject** the loaded pattern snippets together with the user prose into the Socratic (spec-writing) LLM.

Index-driven retrieval like this keeps the library scalable and reproducible; see the pattern and trigger reference docs for the formal metadata grammar.

## Socratic LLM behavior

When driving a Socratic spec-writing loop, an integrator-friendly pattern is:

- Translate prose into **structured specs** using the patterns provided in the injected block, rather than inventing new patterns on the fly.
- Delay finalizing a spec until the human explicitly asks to build or confirms (for example, after \"anything else to add?\"). If the human adds context, reopen the question loop, then confirm again before building.
- **Surface edge cases** explicitly: when a pattern requires a decision that the prose does not specify (for example, who may mutate a resource or whether a role bypasses an invariant), emit a `SpecProposal` or `SpecAmbiguityDetected` event with candidate interpretations and their impact, and wait for human input.
- If a concept has no matching pattern, prefer emitting `SpecAmbiguityDetected` over guessing.
- When multiple patterns apply, consider security and authorization first, then invariants and state legality, then write ownership, then domain and boundaries, then retries and idempotency, then acceptance and UX. The global value hierarchy itself is encoded in `precedence_hierarchy` in `FITPAC/master_index.yaml`.

The spec schema and structured content are described in [Spec schema](../reference/spec-schema.md); for the formal pattern and trigger grammar, see the reference docs that implement RFC-0003 and RFC-0005.
