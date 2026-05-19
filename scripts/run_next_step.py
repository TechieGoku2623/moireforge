#!/usr/bin/env python3
"""Next-step validation: yield Monte Carlo + benchmark sanity."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solutions.yield_optimization import yield_with_redundancy
from sim.performance_benchmark import run_benchmark
from sim.moire_physics import bandgap_meV


def main() -> None:
    print("Next-step validation")
    y = yield_with_redundancy(16, 4, 0.91, trials=3000, seed=7)
    print(f"  yield P(ok) 16+4 @ p=0.91: {y:.3f}")
    assert y > 0.7
    bg = bandgap_meV(1.08)
    print(f"  bandgap @ 1.08 deg: {bg:.2f} meV")
    print()
    run_benchmark()


if __name__ == "__main__":
    main()
