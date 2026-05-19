#!/usr/bin/env python3
"""Write results/benchmark_report.txt from performance model."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.performance_benchmark import run_benchmark


def main() -> None:
    buf = io.StringIO()
    with redirect_stdout(buf):
        run_benchmark()
    text = buf.getvalue()
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "benchmark_report.txt"
    out_file.write_text(text, encoding="utf-8")
    print(f"Wrote {out_file}")
    print(text)


if __name__ == "__main__":
    main()
