#!/usr/bin/env python3
"""Next-step validation: defect yield + bandgap envelope + benchmark sanity."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solutions.yield_optimization import yield_with_defects, yield_with_redundancy
from sim.performance_benchmark import run_benchmark
from sim.moire_physics import bandgap_envelope_meV


def main() -> None:
    print("Next-step validation")
    y = yield_with_redundancy(16, 4, 0.91, trials=3000, seed=7)
    print(f"  binary yield P(ok) 16+4 @ p=0.91: {y:.3f}")
    assert y > 0.7
    d = yield_with_defects(16, 8, p_defective=0.15, p_marginal=0.10, trials=4000, seed=7)
    print(
        f"  defect yield P(ok) 16+8 @ 15%/10%: {d.p_system_ok:.3f} "
        f"(mean good={d.mean_good:.1f})"
    )
    assert d.p_system_ok >= 0.0
    env = bandgap_envelope_meV(1.08)
    print(
        f"  bandgap @ 1.08 deg: {env.nominal_meV:.2f} meV "
        f"(envelope {env.low_meV:.2f}-{env.high_meV:.2f})"
    )
    print()
    run_benchmark()


if __name__ == "__main__":
    main()
