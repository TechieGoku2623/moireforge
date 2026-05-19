"""
Moiré logic cell abstraction: excitonic states mapped to Boolean logic.

Provides NAND/NOR/NOT truth tables consistent with the README narrative.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Iterable


class GateType(IntEnum):
    NAND = 0
    NOR = 1
    NOT = 2


@dataclass(frozen=True)
class LogicState:
    """Excitonic occupancy proxy: high = conducting / logic 1."""

    exciton_occupancy: float  # 0..1

    def to_bit(self, thresh: float = 0.5) -> int:
        return 1 if self.exciton_occupancy >= thresh else 0


def occupancy_from_inputs(inputs: Iterable[int], gate: GateType, *, noise: float = 0.0) -> float:
    """Map binary inputs to normalized output occupancy (deterministic + optional noise)."""
    bits = [1 if int(x) else 0 for x in inputs]
    if gate == GateType.NOT:
        assert len(bits) == 1
        base = 1.0 - bits[0]
    elif gate == GateType.NAND:
        assert len(bits) >= 1
        base = 0.0 if all(b == 1 for b in bits) else 1.0
    elif gate == GateType.NOR:
        assert len(bits) >= 1
        base = 1.0 if all(b == 0 for b in bits) else 0.0
    else:
        raise ValueError(f"Unknown gate {gate}")
    return float(max(0.0, min(1.0, base + noise)))


def truth_table_nand(n_inputs: int = 2) -> list[tuple[tuple[int, ...], int]]:
    """Return (inputs tuple, output bit) for NAND."""
    rows: list[tuple[tuple[int, ...], int]] = []
    from itertools import product

    for combo in product((0, 1), repeat=n_inputs):
        out = 0 if all(c == 1 for c in combo) else 1
        rows.append((combo, out))
    return rows


def print_nand_truth_table(n_inputs: int = 2) -> None:
    rows = truth_table_nand(n_inputs)
    print(f"Moiré NAND truth table ({n_inputs}-input)")
    print("inputs -> out (excitonic model matches Boolean NAND)")
    for ins, out in rows:
        ins_s = "".join(str(x) for x in ins)
        occ = occupancy_from_inputs(ins, GateType.NAND)
        print(f"  {ins_s} -> {out}  (occ={occ:.3f})")


def main() -> None:
    print_nand_truth_table(2)


if __name__ == "__main__":
    main()
