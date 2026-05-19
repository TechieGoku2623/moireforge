#!/usr/bin/env python3
"""Print dev setup hints (deps from requirements.txt)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    req = ROOT / "requirements.txt"
    print("MoiréForge dev environment")
    print(f"  pip install -r {req.relative_to(ROOT)}")
    print("  Optional Verilog: install Icarus Verilog, then `make verilog`")
    print("  Frontend: cd frontend && npm install && npm run dev")


if __name__ == "__main__":
    main()
