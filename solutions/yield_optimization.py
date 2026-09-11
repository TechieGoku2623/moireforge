"""Yield: redundant tiles and defect-aware mapping."""

from __future__ import annotations

import random
from dataclasses import dataclass

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


@dataclass(frozen=True)
class DefectYieldResult:
    p_system_ok: float
    mean_good: float
    mean_marginal: float
    mean_defective: float
    trials: int
    seed: int


def yield_with_defects(
    n_required: int,
    n_spare: int,
    *,
    p_defective: float = 0.15,
    p_marginal: float = 0.10,
    count_marginal_as_good: bool = False,
    trials: int = 5_000,
    seed: int | None = None,
) -> DefectYieldResult:
    """
    Three-state tile model: good / marginal / defective.

    By default only fully good tiles count toward n_required. Set
    count_marginal_as_good=True to treat marginal tiles as usable after binning.
    """
    if p_defective < 0 or p_marginal < 0 or p_defective + p_marginal > 1:
        raise ValueError("p_defective and p_marginal must be >=0 and sum to <= 1")
    s = DEFAULT_MC_SEED if seed is None else int(seed)
    rng = random.Random(s)
    n_total = n_required + n_spare
    ok = 0
    sum_good = 0
    sum_marg = 0
    sum_def = 0
    for _ in range(trials):
        good = marg = bad = 0
        for _tile in range(n_total):
            u = rng.random()
            if u < p_defective:
                bad += 1
            elif u < p_defective + p_marginal:
                marg += 1
            else:
                good += 1
        usable = good + (marg if count_marginal_as_good else 0)
        if usable >= n_required:
            ok += 1
        sum_good += good
        sum_marg += marg
        sum_def += bad
    return DefectYieldResult(
        p_system_ok=ok / trials,
        mean_good=sum_good / trials,
        mean_marginal=sum_marg / trials,
        mean_defective=sum_def / trials,
        trials=trials,
        seed=s,
    )


def main() -> None:
    p_good = 0.92
    print("Binary good/bad yield:")
    for spare in (0, 2, 4, 8):
        y = yield_with_redundancy(16, spare, p_good, seed=DEFAULT_MC_SEED)
        print(f"  16+{spare} tiles, p_die={p_good}: P(system ok) ~ {y:.3f}")
    print("Defect injection (15% defective, 10% marginal):")
    for spare in (0, 4, 8):
        r = yield_with_defects(16, spare, p_defective=0.15, p_marginal=0.10, seed=DEFAULT_MC_SEED)
        print(
            f"  16+{spare}: P(ok)={r.p_system_ok:.3f} "
            f"(mean good={r.mean_good:.1f}, marg={r.mean_marginal:.1f}, def={r.mean_defective:.1f})"
        )
    assert yield_with_redundancy(8, 4, 0.95, trials=2000, seed=1) > 0.99
    assert yield_with_defects(16, 8, p_defective=0.15, p_marginal=0.10, trials=2000, seed=1).p_system_ok >= 0.0


if __name__ == "__main__":
    main()
