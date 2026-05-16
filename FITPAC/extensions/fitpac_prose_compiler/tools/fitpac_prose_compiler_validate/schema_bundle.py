from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from fitpac_prose_compiler_validate.paths import schema_dir


def _load_schemas(directory: Path) -> Registry:
    reg: Registry | None = None
    for path in sorted(directory.glob("*.json")):
        contents = json.loads(path.read_text(encoding="utf-8"))
        uri = contents.get("$id")
        if not uri:
            raise ValueError(f"Schema missing $id: {path}")
        resource = Resource.from_contents(contents)
        reg = reg.with_resource(uri, resource) if reg else Registry().with_resource(uri, resource)
    if reg is None:
        raise FileNotFoundError(f"No JSON schemas in {directory}")
    return reg


def get_validator(schema_name: str, pack: str | Path) -> Draft202012Validator:
    sdir = schema_dir(pack)
    reg = _load_schemas(sdir)
    path = sdir / schema_name
    if not path.is_file():
        raise FileNotFoundError(path)
    root = json.loads(path.read_text(encoding="utf-8"))
    return Draft202012Validator(root, registry=reg)
