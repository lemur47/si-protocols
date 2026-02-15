"""FastAPI application for si-protocols threat analysis.

Run locally only — never host or analyse third-party content.
"""

from __future__ import annotations

import dataclasses
import json

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.schemas import AnalyseRequest, AnalyseResponse, HealthResponse
from si_protocols.threat_filter import hybrid_score


def _escape_control_chars_in_json_strings(raw: str) -> str:
    """Escape literal control characters inside JSON string values.

    Walks the raw JSON text character-by-character, tracking whether the
    current position is inside a quoted string.  Only control characters
    found *inside* a string are replaced with their escape sequences;
    structural whitespace between tokens is left untouched.
    """
    result: list[str] = []
    in_string = False
    i = 0
    while i < len(raw):
        char = raw[i]
        if char == "\\" and in_string:
            # Escaped pair — emit both characters verbatim.
            result.append(char)
            if i + 1 < len(raw):
                result.append(raw[i + 1])
                i += 2
            else:
                i += 1
            continue
        if char == '"':
            in_string = not in_string
        elif in_string:
            if char == "\n":
                result.append("\\n")
                i += 1
                continue
            if char == "\r":
                result.append("\\r")
                i += 1
                continue
            if char == "\t":
                result.append("\\t")
                i += 1
                continue
        result.append(char)
        i += 1
    return "".join(result)


class SanitiseJsonMiddleware(BaseHTTPMiddleware):
    """Middleware that fixes literal newlines inside JSON string values.

    Swagger UI (/docs) lets users paste multiline text into the request
    body textarea.  The resulting JSON contains unescaped newlines inside
    string values, which is invalid per RFC 8259.  This middleware detects
    the parse failure and retries after escaping control characters.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        content_type = request.headers.get("content-type", "")
        if request.method in {"POST", "PUT", "PATCH"} and "application/json" in content_type:
            body = await request.body()
            try:
                json.loads(body)
            except (json.JSONDecodeError, UnicodeDecodeError):
                fixed = _escape_control_chars_in_json_strings(
                    body.decode("utf-8", errors="replace")
                )
                request._body = fixed.encode("utf-8")
        return await call_next(request)


app = FastAPI(
    title="si-protocols API",
    description=(
        "Hybrid tech-psychic threat filter for spiritual intelligence. "
        "Local-only — never host or analyse third-party content."
    ),
    version="0.1.0",
)
app.add_middleware(SanitiseJsonMiddleware)


@app.get("/health")
async def health() -> HealthResponse:
    """Liveness check."""
    return HealthResponse(status="ok")


@app.post("/analyse")
def analyse(request: AnalyseRequest) -> AnalyseResponse:
    """Analyse text for spiritual disinformation markers.

    Sync endpoint — FastAPI runs CPU-bound spaCy work in a thread pool.
    """
    result = hybrid_score(request.text, request.density_bias, seed=request.seed)
    return AnalyseResponse(**dataclasses.asdict(result))


def main() -> None:
    """Entry point: ``python -m app.main``."""
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
