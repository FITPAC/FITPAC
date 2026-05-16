from __future__ import annotations

import json
from pathlib import Path

import pytest

from fitpac_prose_compiler_validate.validate import ValidationError, validate_graph_document

FIXTURES = Path(__file__).resolve().parent / "fixtures"
PACK = Path(__file__).resolve().parents[2]  # FITPAC/extensions/fitpac_prose_compiler/


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_valid_minimal_graph():
    validate_graph_document(_load("valid_minimal_graph.json"), PACK)


def test_illegal_committed_edge():
    with pytest.raises(ValidationError):
        validate_graph_document(_load("illegal_committed_edge.json"), PACK)


def test_partial_missing_flags():
    with pytest.raises(ValidationError):
        validate_graph_document(_load("partial_missing_flags.json"), PACK)


def test_unknown_inventory_id():
    with pytest.raises(ValidationError):
        validate_graph_document(_load("unknown_inventory_id.json"), PACK)


def test_open_resolution_blocks_ready():
    with pytest.raises(ValidationError):
        validate_graph_document(_load("open_resolution_blocks_ready.json"), PACK)


def test_suggested_edge_only_in_resolution_ok():
    """Committed false edges may use non-auto kinds — graph with no committed bad edges."""
    doc = _load("valid_minimal_graph.json")
    doc = dict(doc)
    doc["id"] = "g_suggested"
    doc["edges"] = [
        {
            "id": "e_sug",
            "from_node_id": "n1",
            "to_node_id": "n2",
            "kind": "depends_on",
            "committed": False,
            "provenance": {"user_resolution_id": "u1"},
        }
    ]
    validate_graph_document(doc, PACK)
