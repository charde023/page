"""
frontmatter.py — YAML frontmatter parser (adapted from wisper-page/workflow/lib/frontmatter.py).

Public API:
    split_frontmatter(text: str) -> tuple[dict, str]

Returns (meta_dict, body_text). body_text has leading blank lines stripped.
Returns ({}, text) when no valid '---' frontmatter fence is found.
"""

from __future__ import annotations

import re
from typing import Any


def _parse_frontmatter_manual(fm_text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for raw_line in fm_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and (
            (value[0] == '"' and value[-1] == '"')
            or (value[0] == "'" and value[-1] == "'")
        ):
            value = value[1:-1]
        result[key] = value
    return result


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.lstrip("﻿").startswith("---"):
        return {}, text

    stripped = text.lstrip("﻿")
    first_newline = stripped.find("\n")
    if first_newline == -1:
        return {}, text
    opening_line = stripped[:first_newline].rstrip()
    if opening_line != "---":
        return {}, text

    rest = stripped[first_newline + 1:]

    close_match = re.search(r"^---\s*$", rest, re.MULTILINE)
    if close_match is None:
        return {}, text

    fm_text = rest[: close_match.start()]
    body = rest[close_match.end():]
    body = body.lstrip("\n")

    try:
        import yaml  # type: ignore[import]
        meta = yaml.safe_load(fm_text)
        if not isinstance(meta, dict):
            meta = {}
    except Exception:
        meta = _parse_frontmatter_manual(fm_text)

    return {k: _stringify(v) for k, v in meta.items()}, body


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)
