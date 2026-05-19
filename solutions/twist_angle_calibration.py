"""Post-fabrication twist angle estimation and bandgap targeting."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow `python solutions/foo.py` and package imports
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from sim.moire_physics import bandgap_meV, moire_period_nm


def estimate_twist_from_period(period_nm: float, a_nm: float = 0.246) -> float:
    """Invert small-angle moiré period relation (degrees, approximate)."""
    if period_nm <= 0:
        return 0.0
    import math

    s = a_nm / (2.0 * period_nm)
    s = min(0.999, max(1e-9, s))
    return 2.0 * math.degrees(math.asin(s))


def main() -> None:
    p_nm = 13.4  # example measured period
    twist_guess = estimate_twist_from_period(p_nm)
    eg = bandgap_meV(twist_guess)
    print("Twist angle calibration (demo)")
    print(f"  measured period ~ {p_nm} nm -> twist ~ {twist_guess:.3f} deg")
    print(f"  model bandgap ~ {eg:.2f} meV")
    assert 0.5 < twist_guess < 3.0
    assert eg >= 0


if __name__ == "__main__":
    main()
