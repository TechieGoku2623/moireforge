"""
AI workload performance comparison: Moiré SoC vs CMOS / GPU / TPU / neuromorphic.

All outputs are model-based and intended for architecture exploration.
Two Moire modes are exposed:
1) physics_target: optimistic research target envelope.
2) conservative: guarded envelope for planning and risk analysis.

System power includes fixed + per-tile overheads (CPU/control, NoC, SRAM, DRAM I/F, leakage).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from sim.config_loader import load_calibration


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


@dataclass(frozen=True)
class SystemOverhead:
    """Watts of non-accelerator power. Loaded from config when present."""

    cpu_control_w: float = 0.8
    noc_base_w: float = 0.3
    noc_per_tile_w: float = 0.05
    sram_base_w: float = 0.4
    sram_per_tile_w: float = 0.03
    dram_if_w: float = 1.2
    leakage_base_w: float = 0.2
    leakage_per_tile_w: float = 0.02

    def watts_for_tiles(self, tiles: int) -> float:
        t = max(0, int(tiles))
        return (
            self.cpu_control_w
            + self.noc_base_w
            + self.noc_per_tile_w * t
            + self.sram_base_w
            + self.sram_per_tile_w * t
            + self.dram_if_w
            + self.leakage_base_w
            + self.leakage_per_tile_w * t
        )


def system_overhead() -> SystemOverhead:
    cal = load_calibration()
    raw = cal.get("system_overhead_w")
    if not isinstance(raw, dict):
        return SystemOverhead()
    defaults = SystemOverhead()
    vals = {}
    for field in defaults.__dataclass_fields__:
        v = raw.get(field, getattr(defaults, field))
        vals[field] = float(v)
    return SystemOverhead(**vals)


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
            note="Optimistic accelerator envelope; system overhead still applied.",
        )
    return ModeAssumptions(
        name="conservative",
        tops_per_tile=4.0,
        power_tile_w=2.0,
        note="Guarded accelerator envelope for risk-aware planning; system overhead applied.",
    )


def moire_summary(
    work: Workload,
    mode: Literal["physics_target", "conservative"],
) -> dict[str, dict[str, float]]:
    a = mode_assumptions(mode)
    oh = system_overhead()
    rows: dict[str, dict[str, float]] = {}
    for label, cfg in moire_configs().items():
        tiles = int(cfg["tiles"])
        tops = tiles * a.tops_per_tile
        accel_power = tiles * a.power_tile_w
        overhead = oh.watts_for_tiles(tiles)
        system_power = accel_power + overhead
        accel_eff = tops / accel_power if accel_power > 0 else 0.0
        system_eff = tops / system_power if system_power > 0 else 0.0
        rows[label] = {
            "tiles": float(tiles),
            "tops": tops,
            "accel_power_w": accel_power,
            "overhead_w": overhead,
            "power_w": system_power,  # system power (backward-compatible key)
            "tops_per_w": system_eff,  # system efficiency (primary reported)
            "accel_tops_per_w": accel_eff,
            "system_tops_per_w": system_eff,
            "latency_ms": latency_ms(work.gops_per_inference, tops),
        }
    return rows


def run_benchmark(work: Workload | None = None) -> None:
    work = work or Workload("ResNet-50 (INT8)", 4.0)
    oh = system_overhead()
    print(f"Workload: {work.name}")
    print(f"  Operations per inference: {work.gops_per_inference:.2f} GOp")
    print(
        "  System overhead model (W): "
        f"CPU={oh.cpu_control_w}, NoC_base={oh.noc_base_w}, DRAM_IF={oh.dram_if_w}, ..."
    )
    print()
    for mode in ("physics_target", "conservative"):
        assump = mode_assumptions(mode)
        print(f"Moiré SoC Configurations ({mode}):")
        print(f"  Assumption: {assump.note}")
        for label, vals in moire_summary(work, mode).items():
            print(f"  {label}:")
            print(f"    Throughput: {vals['tops']:.2f} TOPS")
            print(f"    Accel Power: {vals['accel_power_w']:.2f} W")
            print(f"    Overhead Power: {vals['overhead_w']:.2f} W")
            print(f"    System Power: {vals['power_w']:.2f} W")
            print(f"    Accel Efficiency: {vals['accel_tops_per_w']:.2f} TOPS/W")
            print(f"    System Efficiency: {vals['system_tops_per_w']:.2f} TOPS/W")
            print(f"    Latency: {vals['latency_ms']:.2f} ms")
        print()
    print("Reference platforms (model row):")
    for p in reference_platforms():
        lat = latency_ms(work.gops_per_inference, p.tops)
        print(
            f"  {p.name}: ~{p.tops:.0f} TOPS, ~{p.tops_per_w:.1f} TOPS/W, "
            f"~{lat:.2f} ms @ {p.power_w:.1f} W"
        )


def main() -> None:
    run_benchmark()


if __name__ == "__main__":
    main()
