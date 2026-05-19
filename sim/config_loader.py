"""Load optional `config/calibration.json`; defaults match hard-coded demo physics."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_CAL_FILE = ROOT / "config" / "calibration.json"

_DEFAULT_BANDGAP = {
    "magic_angle_deg": 1.08,
    "gaussian_width_deg": 0.35,
    "coupling_scale_meV": 110.0,
    "field_coefficient": 2.5,
}


@lru_cache(maxsize=1)
def load_calibration() -> dict:
    if not _CAL_FILE.exists():
        return {}
    try:
        data = json.loads(_CAL_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def lattice_a_nm() -> float:
    cal = load_calibration()
    v = cal.get("lattice_a_nm")
    return float(v) if isinstance(v, (int, float)) else 0.246


def bandgap_params() -> dict:
    cal = load_calibration()
    bg = cal.get("bandgap")
    if isinstance(bg, dict):
        out = {**_DEFAULT_BANDGAP}
        for k in _DEFAULT_BANDGAP:
            if k in bg and isinstance(bg[k], (int, float)):
                out[k] = float(bg[k])
        return out
    return dict(_DEFAULT_BANDGAP)


def default_mc_seed() -> int:
    cal = load_calibration()
    mc = cal.get("monte_carlo")
    if isinstance(mc, dict) and "default_seed" in mc:
        try:
            return int(mc["default_seed"])
        except (TypeError, ValueError):
            pass
    return 42
