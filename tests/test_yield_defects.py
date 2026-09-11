from solutions.yield_optimization import yield_with_defects


def test_spares_improve_defect_yield():
    a = yield_with_defects(16, 0, p_defective=0.15, p_marginal=0.10, trials=5000, seed=2)
    b = yield_with_defects(16, 8, p_defective=0.15, p_marginal=0.10, trials=5000, seed=2)
    assert b.p_system_ok >= a.p_system_ok


def test_marginal_binning_helps():
    strict = yield_with_defects(
        16, 4, p_defective=0.15, p_marginal=0.10, count_marginal_as_good=False, trials=4000, seed=3
    )
    binned = yield_with_defects(
        16, 4, p_defective=0.15, p_marginal=0.10, count_marginal_as_good=True, trials=4000, seed=3
    )
    assert binned.p_system_ok >= strict.p_system_ok
