"""Adaptive temperature management: throttle tiles vs junction temperature."""

from __future__ import annotations

import math


def dvfs_scale_freq(t_junction_c: float, t_max_c: float = 85.0) -> float:
    """Return 0..1 frequency scale; rolls off above threshold."""
    if t_junction_c <= t_max_c - 15:
        return 1.0
    x = (t_junction_c - (t_max_c - 15)) / 15.0
    return float(max(0.4, 1.0 / (1.0 + math.exp(4 * (x - 0.5)))))


def active_tiles_vs_temp(n_tiles: int, t_junction_c: float, t_max_c: float = 85.0) -> int:
    s = dvfs_scale_freq(t_junction_c, t_max_c)
    return max(1, int(round(n_tiles * s)))


def main() -> None:
    n = 16
    for t in (45, 75, 82, 90):
        ft = dvfs_scale_freq(t)
        nt = active_tiles_vs_temp(n, t)
        print(f"  T={t}C: freq_scale={ft:.2f}, active_tiles={nt}/{n}")
    assert dvfs_scale_freq(50) >= 0.99
    assert active_tiles_vs_temp(16, 90) >= 1


if __name__ == "__main__":
    main()
