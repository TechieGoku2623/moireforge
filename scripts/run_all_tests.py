#!/usr/bin/env python3
"""Run pytest on tests/ unless pytest is missing (then minimal smoke)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pytest", str(ROOT / "tests"), "-q", "--tb=short"],
            cwd=ROOT,
        )
        return int(r.returncode)
    except FileNotFoundError:
        print("pytest not found; running import smoke tests...")
        sys.path.insert(0, str(ROOT))
        import sim.moire_physics  # noqa: F401
        import sim.moire_logic_cell  # noqa: F401
        import sim.performance_benchmark  # noqa: F401

        print("OK (smoke)")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
