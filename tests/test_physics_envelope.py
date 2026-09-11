from sim.moire_physics import bandgap_envelope_meV


def test_envelope_brackets_nominal():
    env = bandgap_envelope_meV(1.08)
    assert env.low_meV <= env.nominal_meV <= env.high_meV
    assert env.high_meV > env.nominal_meV
