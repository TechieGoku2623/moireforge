"""Defect-cluster sensitivity (lightweight)."""

from solutions.yield_optimization import yield_with_redundancy


def test_high_yield_tile_count():
    y = yield_with_redundancy(16, 8, 0.97, trials=5000, seed=3)
    assert y > 0.999
