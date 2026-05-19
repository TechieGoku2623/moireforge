"""Minimal Python SDK for deploying model sizing hints to the Moiré stack."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InferenceJob:
    name: str
    gops: float


def recommend_tiles(job: InferenceJob, tops_per_tile: float = 12.8) -> int:
    """Return integer tile count to cover peak TOPS (upper bound)."""
    import math

    need = job.gops / 1000.0  # GOp -> rough TOPS scale for demo
    return max(1, int(math.ceil(need / max(tops_per_tile, 1e-6))))
