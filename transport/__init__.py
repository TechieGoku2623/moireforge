"""Quantum-aware transport helpers (ballistic / tunneling order-of-magnitude)."""

from __future__ import annotations

import math


def ballistic_conductance_quantum(n_modes: int = 1) -> float:
    """Return G in units of G0 (2e^2/h), counting spin-degenerate channels as n_modes."""
    return float(max(0, int(n_modes)))


def tunnel_probability(barrier_eV: float, width_nm: float, mass_m0: float = 1.0) -> float:
    """
    WKB-like exponential tunneling probability (dimensionless, 0..1).

    Simplified: kappa ~ sqrt(2 m V) / hbar with rough nm/eV scaling constant.
    """
    if barrier_eV <= 0 or width_nm <= 0:
        return 1.0
    kappa_per_nm = 10.0 * math.sqrt(max(barrier_eV, 0.0) * max(mass_m0, 1e-6))
    return float(math.exp(-2.0 * kappa_per_nm * width_nm))


def main() -> None:
    print("Transport demos")
    print(f"  ballistic modes=4 -> {ballistic_conductance_quantum(4):.1f} G0")
    print(f"  tunnel V=0.2eV, w=1nm -> P={tunnel_probability(0.2, 1.0):.3e}")


if __name__ == "__main__":
    main()
