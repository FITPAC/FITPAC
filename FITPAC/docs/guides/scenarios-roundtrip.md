# Scenarios and round-trip (informative)

This page is **informative** only. FITPAC defines the **pattern language** and **consultation protocol**; it does not define where specs, reports, or logs are stored. Orchestration layers (e.g. prose→spec, spec→code, code→spec extraction, spec comparison) and their artifact naming and storage are implementation-defined.

## Scenarios during implementation

During implementation, the coding agent may run **scenarios** — tests or validation steps — to check that the code meets the spec. When a **scenario fails**, treat it like a confidence drop or trigger: consult `FITPAC/master_index.yaml`, classify via `ambiguity_triggers` (e.g. `failed_test`), load only the listed fragments, apply the pattern, and re-evaluate. See [Spec to code](spec-to-code.md) for the consultation procedure.

## Round-trip (extraction and comparison)

The idea of **round-trip** is: (1) produce a structured spec from prose, (2) generate code from that spec, (3) extract a spec from the code using the same schema, (4) compare the two specs. FITPAC defines the **spec schema** (see [Spec schema](../reference/spec-schema.md)) so that comparison is well-defined. Where specs and comparison reports are written, and how iteration or diff reports are named, is defined by your orchestration layer, not by FITPAC.
