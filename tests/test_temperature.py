from solutions.temperature_management import active_tiles_vs_temp, dvfs_scale_freq


def test_dvfs_cool_full_speed():
    assert dvfs_scale_freq(40) >= 0.99


def test_hot_reduces_tiles():
    assert active_tiles_vs_temp(16, 90) < active_tiles_vs_temp(16, 40)
