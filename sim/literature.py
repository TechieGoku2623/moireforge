"""Curated literature anchors for phenomenological model ranges (not a full review)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Citation:
    key: str
    topic: str
    claim: str
    how_used: str
    reference: str
    year: int


def literature_table() -> list[Citation]:
    """
    Anchors used to justify order-of-magnitude model choices.

    These do not calibrate the performance model to silicon; they bound physics
    phenomenology and contextualize edge/neuromorphic efficiency discussions.
    """
    return [
        Citation(
            key="tbg-magic-angle",
            topic="Twisted bilayer graphene magic angle",
            claim="Flat-band / correlated physics near ~1.1° twist.",
            how_used="Sets magic_angle_deg ≈ 1.08 in config/calibration.json.",
            reference="Cao et al., Nature (correlated insulating / superconducting TBG papers)",
            year=2018,
        ),
        Citation(
            key="moire-period",
            topic="Moiré wavelength vs twist",
            claim="lambda_m ≈ a / (2 sin(theta/2)) for small twist.",
            how_used="Implements moire_period_nm() geometric relation.",
            reference="Standard continuum moiré geometry (e.g. Lopes dos Santos / Bistritzer–MacDonald lineage)",
            year=2007,
        ),
        Citation(
            key="tmd-excitons",
            topic="Excitons in 2D TMDs / moiré heterostructures",
            claim="Large exciton binding and long-lived interlayer excitons are common in 2D stacks.",
            how_used="Motivates exciton_binding_meV() heuristic scaling with moiré period.",
            reference="Reviews on TMD excitonics / moiré excitons (e.g. Wang, Mak, Shan lineage)",
            year=2018,
        ),
        Citation(
            key="edge-efficiency",
            topic="Edge AI efficiency context",
            claim="Edge inference is power- and thermal-constrained vs datacenter accelerators.",
            how_used="Motivates conservative vs physics_target dual reporting and system overhead model.",
            reference="Industry edge-AI / MLPerf Tiny / mobile NPU efficiency discussions (contextual)",
            year=2020,
        ),
        Citation(
            key="neuromorphic-efficiency",
            topic="Neuromorphic energy efficiency",
            claim="Event-driven neuromorphic systems can report very high ops/W on sparse workloads.",
            how_used="Provides order-of-magnitude context for Loihi-class reference rows.",
            reference="Intel Loihi / Loihi 2 technical reports and neuromorphic benchmarking literature",
            year=2021,
        ),
    ]


def as_markdown_rows() -> list[str]:
    rows = [
        "| Key | Topic | How used in this repo | Reference (short) | Year |",
        "|-----|-------|----------------------|-------------------|------|",
    ]
    for c in literature_table():
        rows.append(
            f"| `{c.key}` | {c.topic} | {c.how_used} | {c.reference} | {c.year} |"
        )
    return rows
