from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from fitpac_prose_compiler_validate.paths import binding_contract_path, data_dir, profile_path
from fitpac_prose_compiler_validate.schema_bundle import get_validator


@dataclass
class ValidationError(Exception):
    message: str
    path: str = ""

    def __str__(self) -> str:  # pragma: no cover - thin wrapper
        return self.message if not self.path else f"{self.path}: {self.message}"


def _validate_instance(validator: Draft202012Validator, instance: Any) -> None:
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    if errors:
        e = errors[0]
        loc = "/".join(str(x) for x in e.path) if e.path else "<root>"
        raise ValidationError(e.message, loc)


def validate_json_artifact(kind: str, instance: dict[str, Any], pack: str | Path) -> None:
    mapping = {
        "clause": "clause.schema.json",
        "obligation_frame": "obligation_frame.schema.json",
        "normalized_obligation": "normalized_obligation.schema.json",
        "binding_outcome": "binding_outcome.schema.json",
        "resolution_artifact": "resolution_artifact.schema.json",
        "primitive_graph": "primitive_graph.schema.json",
    }
    if kind not in mapping:
        raise ValidationError(f"Unknown artifact kind: {kind}")
    v = get_validator(mapping[kind], pack)
    _validate_instance(v, instance)


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _inventory_ids(data: dict[str, Any]) -> set[str]:
    rows = data.get("rows") or []
    return {str(r["id"]) for r in rows if r.get("id")}


def _load_inventories(pack: str | Path, version: str) -> dict[str, set[str]]:
    d = data_dir(pack, version)
    return {
        "action_sense": _inventory_ids(_load_yaml(d / "action_sense_inventory.yaml")),
        "actor": _inventory_ids(_load_yaml(d / "actor_inventory.yaml")),
        "entity_kind": _inventory_ids(_load_yaml(d / "entity_kind_inventory.yaml")),
    }


def _provenance_nonempty(prov: dict[str, Any] | None) -> bool:
    if not prov or not isinstance(prov, dict):
        return False
    if prov.get("user_resolution_id"):
        return True
    if prov.get("span_ids"):
        return bool(prov["span_ids"])
    if prov.get("frame_ids"):
        return bool(prov["frame_ids"])
    return False


def _binding_contract(pack: str | Path) -> dict[str, Any]:
    return _load_yaml(binding_contract_path(pack))


def _profile(pack: str | Path, profile_id: str) -> dict[str, Any]:
    return _load_yaml(profile_path(pack, profile_id))


def validate_graph_document(
    graph: dict[str, Any],
    pack: str | Path,
    *,
    inventory_version: str = "v0.1.0",
) -> None:
    """Schema + extension conformance for a primitive_graph JSON document."""
    validate_json_artifact("primitive_graph", graph, pack)
    profile_id = graph.get("profile_id")
    if not profile_id:
        raise ValidationError("primitive_graph missing profile_id")
    try:
        profile = _profile(pack, profile_id)
    except FileNotFoundError as exc:
        raise ValidationError(f"Profile not found: {profile_id}") from exc

    _load_inventories(pack, inventory_version)

    auto_kinds = set(profile.get("auto_emittable_edge_kinds") or [])
    allow_partial = bool(profile.get("allow_partial_spine_emission"))
    allow_refines = bool(profile.get("allow_auto_refines_edges"))

    nodes = {n["id"]: n for n in graph.get("nodes", [])}
    for nid, node in nodes.items():
        if node.get("kind") == "spine_primitive":
            if node.get("draft"):
                raise ValidationError("spine_primitive cannot be draft=true", nid)
            bid = node.get("binding_outcome_id")
            if bid:
                # binding outcome object not embedded — optional cross-check skipped
                pass
        if node.get("kind") == "spine_primitive" and not node.get("ontology_primitive_id"):
            raise ValidationError("spine_primitive requires ontology_primitive_id", nid)

    # resolution artifacts: open items block compiler_grade_ready on graph
    open_ids = {
        a["id"]
        for a in graph.get("resolution_artifacts", [])
        if a.get("resolution_status") == "open"
    }

    for edge in graph.get("edges", []):
        if not _provenance_nonempty(edge.get("provenance")):
            raise ValidationError("edge missing provenance pointer", edge.get("id", "?"))
        if edge.get("from_node_id") not in nodes or edge.get("to_node_id") not in nodes:
            raise ValidationError("edge references unknown node", edge.get("id", "?"))
        if edge.get("committed"):
            kind = edge.get("kind")
            allowed = set(auto_kinds)
            if allow_refines:
                allowed.add("refines")
            if kind not in allowed:
                raise ValidationError(
                    f"committed edge kind {kind!r} not allowed by profile auto list",
                    edge.get("id", "?"),
                )

    require_dag = bool(profile.get("require_dag"))
    if require_dag:
        adj = {nid: [] for nid in nodes}
        for edge in graph.get("edges", []):
            if edge.get("committed"):
                adj.setdefault(edge["from_node_id"], []).append(edge["to_node_id"])

        visited: set[str] = set()
        stack: set[str] = set()

        def dfs(u: str) -> None:
            visited.add(u)
            stack.add(u)
            for v in adj.get(u, []):
                if v not in visited:
                    dfs(v)
                elif v in stack:
                    raise ValidationError(f"cycle detected in committed edges involving {u!r}")
            stack.remove(u)

        for nid in nodes:
            if nid not in visited:
                dfs(nid)

    # compiler_grade_ready vs open resolutions
    if graph.get("compiler_grade_ready") and open_ids:
        raise ValidationError(
            f"compiler_grade_ready true but open resolution artifacts: {sorted(open_ids)}"
        )

    for norm in graph.get("normalized_obligations") or []:
        validate_normalized_obligation_integrity(norm, pack, inventory_version=inventory_version)

    for node in graph.get("nodes", []):
        if node.get("kind") != "spine_primitive":
            continue
        if node.get("compiler_grade_ready") is False and graph.get("compiler_grade_ready"):
            raise ValidationError(
                "graph compiler_grade_ready true but node has compiler_grade_ready false",
                node["id"],
            )

    # Enforce partial policy on embedded binding_outcomes if present
    for bo in graph.get("binding_outcomes") or []:
        validate_json_artifact("binding_outcome", bo, pack)
        if bo.get("outcome") == "partial":
            pf = bo.get("partial_flags") or {}
            if pf.get("compiler_grade_ready") is not False:
                raise ValidationError("partial outcome requires compiler_grade_ready false", bo["id"])
            if not allow_partial and not pf.get("draft_spine_emission"):
                raise ValidationError(
                    "partial outcome not allowed for spine unless draft_spine_emission",
                    bo["id"],
                )
        if bo.get("outcome") == "bound":
            norm = next(
                (n for n in graph.get("normalized_obligations") or [] if n["id"] == bo["normalized_obligation_id"]),
                None,
            )
            if norm is None:
                raise ValidationError("bound outcome missing normalized_obligation in graph", bo["id"])
            validate_binding_outcome(bo, norm, pack)


def validate_normalized_obligation_integrity(
    norm: dict[str, Any],
    pack: str | Path,
    *,
    inventory_version: str = "v0.1.0",
) -> None:
    validate_json_artifact("normalized_obligation", norm, pack)
    inv = _load_inventories(pack, inventory_version)
    slots = norm.get("binding_slots") or {}
    status = norm.get("normalization_status")
    for key, inv_key in (
        ("action_sense_id", "action_sense"),
        ("actor_normalized", "actor"),
        ("object_kind", "entity_kind"),
    ):
        val = slots.get(key)
        if val is None:
            continue
        if val not in inv[inv_key] and status == "resolved":
            raise ValidationError(
                f"unknown {key} {val!r} for resolved normalization",
                norm.get("id", "?"),
            )


def validate_binding_outcome(
    outcome: dict[str, Any],
    norm: dict[str, Any],
    pack: str | Path,
) -> None:
    validate_json_artifact("binding_outcome", outcome, pack)
    contract = _binding_contract(pack)
    primitives = contract.get("primitives") or {}
    oid = outcome.get("ontology_primitive_id")
    if outcome.get("outcome") == "bound":
        if not oid:
            raise ValidationError("bound outcome requires ontology_primitive_id", outcome["id"])
        spec = primitives.get(oid)
        if not spec:
            raise ValidationError(f"ontology primitive not in contract: {oid}", outcome["id"])
        slots = (norm.get("binding_slots") or {}) if norm else {}
        for req in spec.get("required_slots", []):
            if slots.get(req) in (None, ""):
                raise ValidationError(f"missing required slot {req}", outcome["id"])
        # forbidden pairs
        for rule in spec.get("forbidden_cooccurrences", []):
            pair = rule.get("pair") or []
            if len(pair) != 2:
                continue
            a, b = pair
            if rule.get("rule") == "if object_kind is null then object_entity_id must be null":
                if slots.get(a) is None and slots.get(b) not in (None, ""):
                    raise ValidationError("forbidden slot combination", outcome["id"])
