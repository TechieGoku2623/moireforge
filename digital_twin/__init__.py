"""Digital twin: aging and defect-rate projection stubs."""

from __future__ import annotations

import math


def aging_factor(years: float, tau_years: float = 10.0) -> float:
    """Multiplicative performance retention after aging (0..1)."""
    if years <= 0:
        return 1.0
    return float(math.exp(-years / max(tau_years, 1e-6)))


def defect_rate_growth(base_rate: float, years: float, growth_per_year: float = 0.02) -> float:
    """Linear growth of defect probability with age, capped at 0.95."""
    return float(min(0.95, max(0.0, base_rate + growth_per_year * years)))


def main() -> None:
    print("Digital twin demos")
    for y in (0, 1, 5, 10):
        print(
            f"  year={y}: aging_factor={aging_factor(y):.3f}, "
            f"defect_rate={defect_rate_growth(0.05, y):.3f}"
        )


if __name__ == "__main__":
    main()
