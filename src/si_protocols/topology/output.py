"""JSON output helper for topology results."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from enum import Enum
from typing import IO, Any

from si_protocols.topology.types import TopologyResult


class _EnumEncoder(json.JSONEncoder):
    """JSON encoder that serialises Enum members to their value."""

    def default(self, o: Any) -> Any:
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


def render_topology_json(result: TopologyResult, *, file: IO[str] | None = None) -> str:
    """Serialise *result* to indented JSON.

    If *file* is given, writes directly to it and returns the JSON string.
    Otherwise writes to stdout.
    """
    data = asdict(result)
    text = json.dumps(data, indent=2, ensure_ascii=False, cls=_EnumEncoder) + "\n"
    dest = file or sys.stdout
    dest.write(text)
    return text
