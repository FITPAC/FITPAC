#!/usr/bin/env python3
"""CLI for validating fitpac.prose_compiler JSON artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from fitpac_prose_compiler_validate.validate import (  # noqa: E402
    ValidationError,
    validate_graph_document,
    validate_json_artifact,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate fitpac.prose_compiler artifacts.")
    parser.add_argument(
        "kind",
        choices=["graph", "clause", "obligation_frame", "normalized_obligation", "binding_outcome", "resolution_artifact"],
    )
    parser.add_argument("--pack", required=True, help="Path to fitpac.prose_compiler extension pack root")
    parser.add_argument("--document", required=True, help="Path to JSON document")
    args = parser.parse_args()
    pack = Path(args.pack).resolve()
    doc_path = Path(args.document).resolve()
    data = json.loads(doc_path.read_text(encoding="utf-8"))
    try:
        if args.kind == "graph":
            validate_graph_document(data, pack)
        else:
            validate_json_artifact(args.kind, data, pack)
    except ValidationError as exc:
        print(f"VALIDATION_ERROR: {exc}", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
