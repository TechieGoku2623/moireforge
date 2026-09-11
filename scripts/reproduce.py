#!/usr/bin/env python3
"""
One-shot reproducibility: tests, simulations, diagrams, benchmark report, manifest.

Run from repo root: python scripts/reproduce.py
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
MANIFEST = RESULTS / "manifest.json"


def _git_rev() -> tuple[str, bool]:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        sha = (r.stdout or "").strip() or "unknown"
        d = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        dirty = bool((d.stdout or "").strip())
        return sha, dirty
    except OSError:
        return "unknown", False


def _run_step(name: str, argv: list[str]) -> None:
    print(f"[reproduce] {name} ...", flush=True)
    r = subprocess.run(argv, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f"[reproduce] FAILED: {name} (exit {r.returncode})")


def main() -> int:
    RESULTS.mkdir(exist_ok=True)

    steps: list[tuple[str, list[str]]] = [
        ("pytest", [sys.executable, "-m", "pytest", str(ROOT / "tests"), "-q", "--tb=short"]),
        ("sim.moire_physics", [sys.executable, "-m", "sim.moire_physics"]),
        ("sim.moire_logic_cell", [sys.executable, "-m", "sim.moire_logic_cell"]),
        ("sim.performance_benchmark", [sys.executable, "-m", "sim.performance_benchmark"]),
        ("solutions.twist_angle_calibration", [sys.executable, str(ROOT / "solutions" / "twist_angle_calibration.py")]),
        ("solutions.temperature_management", [sys.executable, str(ROOT / "solutions" / "temperature_management.py")]),
        ("solutions.yield_optimization", [sys.executable, str(ROOT / "solutions" / "yield_optimization.py")]),
        ("solutions.integration_flow", [sys.executable, str(ROOT / "solutions" / "integration_flow.py")]),
        ("diagrams", [sys.executable, str(ROOT / "scripts" / "generate_diagrams.py")]),
        ("market_comparison", [sys.executable, str(ROOT / "scripts" / "update_market_comparison.py")]),
        ("rtl_lint", [sys.executable, str(ROOT / "scripts" / "lint_rtl.py")]),
        ("benchmark_report", [sys.executable, str(ROOT / "scripts" / "run_benchmark_report.py")]),
        ("transport", [sys.executable, "-c", "import transport; transport.main()"]),
        ("digital_twin", [sys.executable, "-c", "import digital_twin; digital_twin.main()"]),
    ]
    for label, cmd in steps:
        _run_step(label, cmd)

    try:
        import importlib.metadata as im

        pkgs = {}
        for name in ("numpy", "scipy", "matplotlib", "fastapi", "pytest"):
            try:
                pkgs[name] = im.version(name)
            except im.PackageNotFoundError:
                pkgs[name] = None
    except Exception:
        pkgs = {}

    sha, dirty = _git_rev()
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "git_commit": sha,
        "git_dirty": dirty,
        "packages": pkgs,
        "steps_ok": [s[0] for s in steps],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[reproduce] wrote {MANIFEST.relative_to(ROOT)}", flush=True)
    print("[reproduce] OK.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
