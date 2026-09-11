"""
Moiré superlattice physics: period, bandgap vs twist, carrier scales.

Uses continuum / tight-binding-inspired scalings; suitable for framework demos
and calibration hooks (see solutions/twist_angle_calibration.py).

Evidence note: curves are phenomenological. Use bandgap_envelope_meV() for a
literature-style uncertainty band (not a fitted DFT/experiment surrogate).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from sim.config_loader import bandgap_params, lattice_a_nm, load_calibration

# Graphene lattice constant (nm) — overridden by config/calibration.json when present
A_GRAPHEME_NM = lattice_a_nm()


def moire_period_nm(twist_deg: float, a_nm: float = A_GRAPHEME_NM) -> float:
    """Moiré period lambda_m = a / (2 sin(theta/2)) for small angles."""
    rad = math.radians(twist_deg)
    if abs(rad) < 1e-12:
        return float("inf")
    return a_nm / (2.0 * math.sin(abs(rad) / 2.0))


def bandgap_meV(
    twist_deg: float,
    displacement_field_Vnm: float = 0.0,
    coupling_scale_meV: float | None = None,
) -> float:
    """
    Phenomenological tunable gap (meV): peaks near magic angle ~1.08° for TBG-like scaling.

    coupling_scale_meV sets the order of magnitude at the first magic window (from calibration
    file when None). displacement_field_Vnm adds a vertical field term (nm-scale effective).
    """
    bp = bandgap_params()
    if coupling_scale_meV is None:
        coupling_scale_meV = bp["coupling_scale_meV"]
    t = abs(twist_deg)
    magic = bp["magic_angle_deg"]
    width = bp["gaussian_width_deg"]
    peak = coupling_scale_meV * math.exp(-((t - magic) ** 2) / (2 * width**2))
    field_term = bp["field_coefficient"] * abs(displacement_field_Vnm)
    return float(peak + field_term)


@dataclass(frozen=True)
class BandgapEnvelope:
    nominal_meV: float
    low_meV: float
    high_meV: float
    note: str


def bandgap_envelope_meV(
    twist_deg: float,
    displacement_field_Vnm: float = 0.0,
) -> BandgapEnvelope:
    """
    Nominal gap plus relative uncertainty band from config/calibration.json.

    Default band is ±35% around the phenomenological peak to reflect stack/twist
    variation and model form uncertainty (planning envelope, not a fit).
    """
    cal = load_calibration()
    lit = cal.get("literature_envelope") if isinstance(cal.get("literature_envelope"), dict) else {}
    rel = float(lit.get("relative_uncertainty", 0.35))
    note = str(
        lit.get(
            "note",
            "Phenomenological envelope (± relative uncertainty); not silicon-validated.",
        )
    )
    nom = bandgap_meV(twist_deg, displacement_field_Vnm)
    return BandgapEnvelope(
        nominal_meV=nom,
        low_meV=max(0.0, nom * (1.0 - rel)),
        high_meV=nom * (1.0 + rel),
        note=note,
    )


def exciton_binding_meV(moire_nm: float) -> float:
    """Larger superlattice -> softer confinement heuristic (meV)."""
    if moire_nm <= 0 or not math.isfinite(moire_nm):
        return 0.0
    return float(180.0 * (13.0 / max(moire_nm, 1.0)) ** 0.5)


def mobility_cm2Vs(coupling_meV: float, base_mu: float = 150_000.0) -> float:
    """Order-of-magnitude mobility vs coupling (strong coupling reduces somewhat)."""
    return float(base_mu / (1.0 + coupling_meV / 80.0))


def main() -> None:
    twists = np.linspace(0.4, 3.0, 14)
    print("Moiré physics sweep (graphene-like)")
    print(
        f"{'twist_deg':>12} {'period_nm':>12} {'Egap_meV':>12} "
        f"{'low':>10} {'high':>10} {'Ebind_meV':>12} {'mu_cm2/Vs':>14}"
    )
    for tw in twists:
        lm = moire_period_nm(float(tw))
        env = bandgap_envelope_meV(float(tw))
        eb = exciton_binding_meV(lm if math.isfinite(lm) else 13.0)
        mu = mobility_cm2Vs(env.nominal_meV)
        print(
            f"{tw:12.3f} {lm if math.isfinite(lm) else float('nan'):12.3f} "
            f"{env.nominal_meV:12.2f} {env.low_meV:10.2f} {env.high_meV:10.2f} "
            f"{eb:12.2f} {mu:14.1f}"
        )
    print(f"Envelope note: {bandgap_envelope_meV(1.08).note}")


if __name__ == "__main__":
    main()
