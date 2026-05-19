"""Yield: redundant tiles and defect-aware mapping."""

from __future__ import annotations

import random

from sim.config_loader import default_mc_seed

# Documented default for reproducibility (overridable via config/calibration.json)
DEFAULT_MC_SEED = default_mc_seed()


def yield_with_redundancy(
    n_required: int,
    n_spare: int,
    p_good: float,
    *,
    trials: int = 5_000,
    seed: int | None = None,
) -> float:
    """
    Monte Carlo: probability that at least n_required tiles are good among n_required+n_spare.

    If seed is None, uses calibration default (``DEFAULT_MC_SEED``).
    """
    s = DEFAULT_MC_SEED if seed is None else int(seed)
    rng = random.Random(s)
    n_total = n_required + n_spare
    ok = 0
    for _ in range(trials):
        good = sum(1 for _ in range(n_total) if rng.random() < p_good)
        if good >= n_required:
            ok += 1
    return ok / trials


def main() -> None:
    p_good = 0.92
    for spare in (0, 2, 4, 8):
        y = yield_with_redundancy(16, spare, p_good, seed=DEFAULT_MC_SEED)
        print(f"  16+{spare} tiles, p_die={p_good}: P(system ok) ~ {y:.3f}")
    assert yield_with_redundancy(8, 4, 0.95, trials=2000, seed=1) > 0.99


if __name__ == "__main__":
    main()
