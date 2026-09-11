from sim.literature import literature_table
from sim.performance_benchmark import Workload, moire_summary, system_overhead


def test_latency_decreases_with_tops():
    from sim.performance_benchmark import latency_ms

    assert latency_ms(4.0, 200) < latency_ms(4.0, 50)


def test_moire_medium_has_16_tiles():
    from sim.performance_benchmark import moire_configs

    m = moire_configs()["Medium (16 tiles)"]
    assert int(m["tiles"]) == 16


def test_conservative_is_lower_efficiency_than_target():
    work = Workload("ResNet-50 (INT8)", 4.0)
    target = moire_summary(work, "physics_target")["Medium (16 tiles)"]["system_tops_per_w"]
    conservative = moire_summary(work, "conservative")["Medium (16 tiles)"]["system_tops_per_w"]
    assert conservative < target


def test_system_power_exceeds_accel_power():
    work = Workload("ResNet-50 (INT8)", 4.0)
    row = moire_summary(work, "physics_target")["Medium (16 tiles)"]
    assert row["power_w"] > row["accel_power_w"]
    assert row["system_tops_per_w"] < row["accel_tops_per_w"]


def test_overhead_scales_with_tiles():
    oh = system_overhead()
    assert oh.watts_for_tiles(64) > oh.watts_for_tiles(4)


def test_literature_table_nonempty():
    rows = literature_table()
    assert len(rows) >= 5
    keys = {r.key for r in rows}
    assert "tbg-magic-angle" in keys
    assert "moire-period" in keys
