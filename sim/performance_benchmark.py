"""
AI workload performance comparison: Moiré SoC vs CMOS / GPU / TPU / neuromorphic.

All outputs are model-based and intended for architecture exploration.
Two Moire modes are exposed:
1) physics_target: optimistic research target envelope.
2) conservative: guarded envelope for planning and risk analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class PlatformSpec:
    name: str
    tops: float  # peak TOPS (INT8-ish)
    tops_per_w: float
    power_w: float  # active


@dataclass
class Workload:
    name: str
    gops_per_inference: float


@dataclass
class ModeAssumptions:
    name: str
    tops_per_tile: float
    power_tile_w: float
    note: str


def reference_platforms() -> list[PlatformSpec]:
    return [
        PlatformSpec("CMOS (ARM Cortex-A78 class)", tops=4.0, tops_per_w=2.0, power_w=3.0),
        PlatformSpec("GPU (NVIDIA A100 INT8)", tops=624.0, tops_per_w=2.0, power_w=400.0),
        PlatformSpec("TPU v4 (INT8)", tops=275.0, tops_per_w=1.8, power_w=200.0),
        PlatformSpec("Neuromorphic (Loihi 2 scaled)", tops=8.0, tops_per_w=400.0, power_w=0.02),
    ]


def moire_configs() -> dict[str, dict[str, float]]:
    return {
        "Small (4 tiles)": {"tiles": 4},
        "Medium (16 tiles)": {"tiles": 16},
        "Large (64 tiles)": {"tiles": 64},
    }


def latency_ms(gops: float, tops: float) -> float:
    if tops <= 0:
        return float("inf")
    return (gops / tops) * 1e3


def mode_assumptions(mode: Literal["physics_target", "conservative"]) -> ModeAssumptions:
    if mode == "physics_target":
        return ModeAssumptions(
            name="physics_target",
            tops_per_tile=12.8,
            power_tile_w=0.5,
            note="Optimistic envelope tied to model assumptions; not measured silicon.",
        )
    return ModeAssumptions(
        name="conservative",
        tops_per_tile=4.0,
        power_tile_w=2.0,
        note="Guarded planning envelope intended for risk-aware projections.",
    )


def moire_summary(
    work: Workload,
    mode: Literal["physics_target", "conservative"],
) -> dict[str, dict[str, float]]:
    a = mode_assumptions(mode)
    rows: dict[str, dict[str, float]] = {}
    for label, cfg in moire_configs().items():
        tiles = int(cfg["tiles"])
        tops = tiles * a.tops_per_tile
        power = tiles * a.power_tile_w
        eff = tops / power if power > 0 else 0.0
        rows[label] = {
            "tiles": float(tiles),
            "tops": tops,
            "tops_per_w": eff,
            "latency_ms": latency_ms(work.gops_per_inference, tops),
            "power_w": power,
        }
    return rows


def run_benchmark(work: Workload | None = None) -> None:
    work = work or Workload("ResNet-50 (INT8)", 4.0)
    print(f"Workload: {work.name}")
    print(f"  Operations per inference: {work.gops_per_inference:.2f} GOp")
    print()
    for mode in ("physics_target", "conservative"):
        assump = mode_assumptions(mode)
        print(f"Moiré SoC Configurations ({mode}):")
        print(f"  Assumption: {assump.note}")
        for label, vals in moire_summary(work, mode).items():
            print(f"  {label}:")
            print(f"    Throughput: {vals['tops']:.2f} TOPS")
            print(f"    Energy Efficiency: {vals['tops_per_w']:.2f} TOPS/W")
            print(f"    Latency: {vals['latency_ms']:.2f} ms")
            print(f"    Power: {vals['power_w']:.2f} W")
        print()
    print()
    print("Reference platforms (model row):")
    for p in reference_platforms():
        lat = latency_ms(work.gops_per_inference, p.tops)
        print(f"  {p.name}: ~{p.tops:.0f} TOPS, ~{p.tops_per_w:.1f} TOPS/W, ~{lat:.2f} ms @ {p.power_w:.1f} W")


def main() -> None:
    run_benchmark()


if __name__ == "__main__":
    main()
