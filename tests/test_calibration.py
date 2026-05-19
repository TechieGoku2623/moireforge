from sim.moire_physics import bandgap_meV, moire_period_nm
from solutions.twist_angle_calibration import estimate_twist_from_period


def test_period_twist_roundtrip_order():
    tw = 1.1
    p = moire_period_nm(tw)
    tw2 = estimate_twist_from_period(p)
    assert abs(tw2 - tw) < 0.05


def test_bandgap_non_negative():
    assert bandgap_meV(1.08) >= 0
