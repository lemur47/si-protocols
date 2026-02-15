"""Pydantic models for the si-protocols REST API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AnalyseRequest(BaseModel):
    """Request body for POST /analyse."""

    text: str = Field(min_length=1, max_length=100_000)
    density_bias: float = Field(default=0.75, ge=0.0, le=1.0)
    seed: int | None = None


class AnalyseResponse(BaseModel):
    """Response body mirroring ThreatResult fields."""

    overall_threat_score: float
    tech_contribution: float
    intuition_contribution: float
    detected_entities: list[str]
    authority_hits: list[str]
    urgency_hits: list[str]
    emotion_hits: list[str]
    contradiction_hits: list[str]
    source_attribution_hits: list[str]
    escalation_hits: list[str]
    message: str


class HealthResponse(BaseModel):
    """Response body for GET /health."""

    status: str
