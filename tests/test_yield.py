from solutions.yield_optimization import yield_with_redundancy


def test_redundancy_improves():
    a = yield_with_redundancy(8, 0, 0.9, trials=4000, seed=1)
    b = yield_with_redundancy(8, 4, 0.9, trials=4000, seed=1)
    assert b >= a
