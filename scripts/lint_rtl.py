#!/usr/bin/env python3
"""Lightweight RTL hygiene: require STUB/behavioral markers on Verilog modules."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RTL = ROOT / "rtl"
MARKERS = ("behavioral", "stub", "STUB", "architecture-level", "placeholder")


def main() -> int:
    files = sorted(RTL.glob("*.v"))
    if not files:
        print("No RTL files found")
        return 1
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not any(m.lower() in text.lower() for m in MARKERS):
            bad.append(path.name)
    if bad:
        print("RTL files missing stub/behavioral marker:")
        for name in bad:
            print(f"  - {name}")
        return 1
    print(f"RTL lint OK ({len(files)} files have stub/behavioral markers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
