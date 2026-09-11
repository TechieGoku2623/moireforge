#!/usr/bin/env python3
"""Generate architecture / physics diagrams into docs/generated/."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = ROOT / "docs" / "generated"
OUT.mkdir(parents=True, exist_ok=True)


def diagram_bandgap_vs_twist() -> Path:
    from sim.moire_physics import bandgap_envelope_meV

    t = np.linspace(0.2, 4.0, 120)
    envs = [bandgap_envelope_meV(float(x)) for x in t]
    eg = np.array([e.nominal_meV for e in envs])
    low = np.array([e.low_meV for e in envs])
    high = np.array([e.high_meV for e in envs])
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.fill_between(t, low, high, color="#93c5fd", alpha=0.45, label="Uncertainty envelope")
    ax.plot(t, eg, color="#1d4ed8", lw=2, label="Nominal model")
    ax.set_xlabel("Twist angle (deg)")
    ax.set_ylabel("Model bandgap (meV)")
    ax.set_title("Moiré tunable gap with planning envelope")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.text(
        0.02,
        0.02,
        envs[0].note,
        transform=ax.transAxes,
        fontsize=7,
        color="#64748b",
        va="bottom",
    )
    p = OUT / "bandgap_vs_twist.png"
    fig.tight_layout()
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p


def diagram_soc_blocks() -> Path:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis("off")
    blocks = [
        (0.05, 0.55, 0.18, 0.35, "RV32I\nCPU"),
        (0.28, 0.55, 0.22, 0.35, "NoC\nmesh"),
        (0.54, 0.55, 0.22, 0.35, "Moiré\ntiles"),
        (0.78, 0.55, 0.17, 0.35, "PMU"),
        (0.2, 0.1, 0.6, 0.3, "Hybrid memory (SRAM + Moiré cache + DRAM)"),
    ]
    for x, y, w, h, txt in blocks:
        ax.add_patch(
            plt.Rectangle((x, y), w, h, fill=True, facecolor="#e2e8f0", edgecolor="#64748b", lw=1.5)
        )
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=9)
    ax.set_title("Moiré SoC block diagram (conceptual)")
    p = OUT / "soc_block_diagram.png"
    fig.tight_layout()
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return p


def diagram_performance_comparison() -> Path:
    """Bar charts from sim.performance_benchmark with optimistic + conservative modes."""
    from sim.performance_benchmark import Workload, latency_ms, moire_summary, reference_platforms

    work = Workload("ResNet-50 (INT8)", 4.0)
    labels: list[str] = []
    tops_list: list[float] = []
    eff_list: list[float] = []
    lat_list: list[float] = []
    colors: list[str] = []

    moire_target_c = "#0ea5e9"
    moire_conservative_c = "#22c55e"
    ref_c = "#64748b"
    for mode, color, suffix in (
        ("physics_target", moire_target_c, "\n(target)"),
        ("conservative", moire_conservative_c, "\n(conservative)"),
    ):
        for name, vals in moire_summary(work, mode).items():
            labels.append(name.replace(" ", "\n") + suffix)
            tops_list.append(vals["tops"])
            eff_list.append(vals["system_tops_per_w"])
            lat_list.append(vals["latency_ms"])
            colors.append(color)

    for plat in reference_platforms():
        labels.append(plat.name.replace(" ", "\n").replace("(", "\n("))
        tops_list.append(plat.tops)
        eff_list.append(plat.tops_per_w)
        lat_list.append(latency_ms(work.gops_per_inference, plat.tops))
        colors.append(ref_c)

    x = np.arange(len(labels))
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.5))
    fig.suptitle(
        "Model results: system TOPS/W includes CPU/NoC/SRAM/DRAM/leakage overhead",
        fontsize=12,
        fontweight="600",
    )

    def _bars(ax, values, title, ylabel, log=False):
        bars = ax.bar(x, values, color=colors, edgecolor="#1e293b", linewidth=0.6)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=7, rotation=0, ha="center")
        ax.set_title(title, fontsize=10)
        ax.set_ylabel(ylabel)
        ax.grid(True, axis="y", alpha=0.35)
        if log:
            ax.set_yscale("log")
        return bars

    _bars(axes[0], tops_list, "Throughput", "TOPS (log)", log=True)
    _bars(axes[1], eff_list, "System energy efficiency", "System TOPS/W")
    _bars(axes[2], lat_list, "Inferred latency", "ms (lower is better)")

    fig.text(
        0.5,
        0.02,
        "Note: all rows are model-derived. Use conservative mode for planning; validate with measured silicon.",
        ha="center",
        fontsize=8,
        color="#64748b",
    )
    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    p = OUT / "performance_comparison.png"
    fig.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return p


def diagram_problem_solution_map() -> Path:
    """How the framework maps real edge-AI / Moiré integration pain points to repo capabilities."""
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title(
        "Existing problems → what this project provides",
        fontsize=13,
        fontweight="600",
        pad=16,
    )

    problems = [
        (0.35, 7.8, "Edge AI needs\nhigh TOPS/W\nand low idle power"),
        (0.35, 5.5, "Twist / stack\nvariation breaks\npredictable gaps"),
        (0.35, 3.2, "Thermal limits\nthrottle peak\nperformance"),
        (0.35, 0.9, "Defective tiles\nkill yield at\nscale"),
    ]
    solutions = [
        (5.85, 7.8, "Performance model\n+ RTL + PMU stubs\n(benchmark + DVFS hooks)"),
        (5.85, 5.5, "Calibration sim\n(twist ↔ period ↔ gap)\n+ config/calibration.json"),
        (5.85, 3.2, "Temperature mgmt\nsim (active tiles /\nfreq scaling)"),
        (5.85, 0.9, "Yield MC + spare\ntiles (redundancy)\n+ integration checklist"),
    ]

    def box(xy, w, h, text, face, edge="#334155"):
        from matplotlib.patches import FancyBboxPatch

        bx = FancyBboxPatch(
            xy,
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            facecolor=face,
            edgecolor=edge,
            linewidth=1.2,
        )
        ax.add_patch(bx)
        ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=9)

    bw, bh = 4.5, 1.35
    for (px, py, pt), (sx, sy, st) in zip(problems, solutions, strict=True):
        box((px, py), bw, bh, pt, "#fee2e2")
        box((sx, sy), bw, bh, st, "#dcfce7")
        ax.annotate(
            "",
            xy=(sx - 0.05, sy + bh / 2),
            xytext=(px + bw + 0.05, py + bh / 2),
            arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, shrinkA=2, shrinkB=2),
        )

    ax.text(2.55, 9.35, "Industry / integration pain", ha="center", fontsize=10, color="#991b1b")
    ax.text(8.1, 9.35, "This repository", ha="center", fontsize=10, color="#166534")

    fig.text(
        0.5,
        0.02,
        "Run: python scripts/generate_diagrams.py  —  outputs in docs/generated/",
        ha="center",
        fontsize=8,
        color="#64748b",
    )
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    p = OUT / "problem_solution_map.png"
    fig.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return p


def diagram_yield_defects() -> Path:
    from solutions.yield_optimization import yield_with_defects

    spares = [0, 2, 4, 8, 12]
    p_ok = [
        yield_with_defects(16, s, p_defective=0.15, p_marginal=0.10, trials=4000, seed=42).p_system_ok
        for s in spares
    ]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(spares, p_ok, marker="o", color="#059669", lw=2)
    ax.set_xlabel("Spare tiles")
    ax.set_ylabel("P(system OK)")
    ax.set_title("Yield with defects (15% defective, 10% marginal; need 16 good)")
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    p = OUT / "yield_with_defects.png"
    fig.tight_layout()
    fig.savefig(p, dpi=150, facecolor="white")
    plt.close(fig)
    return p


def main() -> None:
    os.environ.setdefault("MPLBACKEND", "Agg")
    p1 = diagram_bandgap_vs_twist()
    p2 = diagram_soc_blocks()
    p3 = diagram_performance_comparison()
    p4 = diagram_problem_solution_map()
    p5 = diagram_yield_defects()
    print(f"Wrote {p1}")
    print(f"Wrote {p2}")
    print(f"Wrote {p3}")
    print(f"Wrote {p4}")
    print(f"Wrote {p5}")


if __name__ == "__main__":
    main()
