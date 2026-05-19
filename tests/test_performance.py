from sim.performance_benchmark import Workload, latency_ms, moire_configs, moire_summary


def test_latency_decreases_with_tops():
    assert latency_ms(4.0, 200) < latency_ms(4.0, 50)


def test_moire_medium_has_16_tiles():
    m = moire_configs()["Medium (16 tiles)"]
    assert int(m["tiles"]) == 16


def test_conservative_is_lower_efficiency_than_target():
    work = Workload("ResNet-50 (INT8)", 4.0)
    target = moire_summary(work, "physics_target")["Medium (16 tiles)"]["tops_per_w"]
    conservative = moire_summary(work, "conservative")["Medium (16 tiles)"]["tops_per_w"]
    assert conservative < target
