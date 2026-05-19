#!/usr/bin/env python3
"""Run tests, next-step validation, and benchmark report in sequence."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    steps = [
        [sys.executable, str(ROOT / "scripts" / "run_all_tests.py")],
        [sys.executable, str(ROOT / "scripts" / "run_next_step.py")],
        [sys.executable, str(ROOT / "scripts" / "run_benchmark_report.py")],
    ]
    for cmd in steps:
        r = subprocess.run(cmd, cwd=ROOT)
        if r.returncode != 0:
            return int(r.returncode)
    print("Pipeline OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
