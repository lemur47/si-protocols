---
title: REST API Reference
description: Analyse text over HTTP with the FastAPI-based si-protocols API.
order: 3
---

## Running the Server

```bash
# Install dependencies (if not done already)
uv sync --all-extras
uv pip install en_core_web_sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl

# Start the API server
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The server binds to `127.0.0.1` only — it is designed for local use. Never expose it to the public internet or use it to analyse third-party content.

## Interactive Docs

Once the server is running, open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the Swagger UI. You can paste text directly into the request body and execute requests from the browser.

Multiline text is supported — a sanitising middleware escapes literal newlines inside JSON string values so you can paste passages without manual escaping.

## Endpoints

### `GET /health`

Liveness check.

**Response:**

```json
{
  "status": "ok"
}
```

**Example:**

```bash
curl http://127.0.0.1:8000/health
```

### `POST /analyse`

Analyse text for spiritual disinformation markers. This is a synchronous endpoint — FastAPI runs the CPU-bound spaCy work in a thread pool.

**Request body:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `text` | `string` | Yes | — | Text to analyse (1–100,000 characters) |
| `density_bias` | `float` | No | `0.75` | Information density bias for heuristic layer (0.0–1.0) |
| `seed` | `int \| null` | No | `null` | RNG seed for reproducible heuristic scores |

**Response body:**

| Field | Type | Description |
|-------|------|-------------|
| `overall_threat_score` | `float` | Hybrid score (0–100) |
| `tech_contribution` | `float` | Tech layer score (0–100) |
| `intuition_contribution` | `float` | Heuristic layer score |
| `detected_entities` | `list[str]` | Named entities found by spaCy |
| `authority_hits` | `list[str]` | Matched authority claim phrases |
| `urgency_hits` | `list[str]` | Matched urgency/fear patterns |
| `emotion_hits` | `list[str]` | Matched fear and euphoria words/phrases |
| `contradiction_hits` | `list[str]` | Detected contradiction pair labels |
| `source_attribution_hits` | `list[str]` | Unfalsifiable and unnamed authority phrases |
| `escalation_hits` | `list[str]` | Commitment escalation labels by segment |
| `message` | `str` | Disclaimer |

**Example request:**

```bash
curl -X POST http://127.0.0.1:8000/analyse \
  -H "Content-Type: application/json" \
  -d '{"text": "The ascended masters say you must act now. Time is running out.", "seed": 42}'
```

**Example response:**

```json
{
  "overall_threat_score": 27.74,
  "tech_contribution": 23.36,
  "intuition_contribution": 34.31,
  "detected_entities": [],
  "authority_hits": ["the ascended masters say"],
  "urgency_hits": ["you must act now", "time is running out"],
  "emotion_hits": [],
  "contradiction_hits": [],
  "source_attribution_hits": [],
  "escalation_hits": [],
  "message": "Run on your own texts only — this is a local tool."
}
```

## Error Handling

The API returns **422 Unprocessable Entity** for validation errors, such as:

- Empty `text` field
- `density_bias` outside the 0.0–1.0 range
- `text` exceeding 100,000 characters

Errors follow Pydantic's validation error format:

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "text"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {"min_length": 1}
    }
  ]
}
```
