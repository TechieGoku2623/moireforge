"""FastAPI app: health, physics sweep, benchmark summary."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sim.moire_physics import bandgap_meV, moire_period_nm
from sim.performance_benchmark import mode_assumptions, moire_configs, moire_summary, reference_platforms, Workload

app = FastAPI(title="MoiréForge API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Health(BaseModel):
    ok: bool = True
    service: str = "moire-forge"


class SweepIn(BaseModel):
    twist_start: float = Field(0.5, ge=0.01, le=10)
    twist_end: float = Field(3.0, ge=0.01, le=10)
    points: int = Field(20, ge=3, le=200)


@app.get("/health", response_model=Health)
def health() -> Health:
    return Health()


@app.post("/physics/sweep")
def physics_sweep(body: SweepIn) -> dict:
    import numpy as np

    t = np.linspace(body.twist_start, body.twist_end, body.points)
    rows = []
    for x in t:
        tw = float(x)
        p = moire_period_nm(tw)
        eg = bandgap_meV(tw)
        rows.append({"twist_deg": tw, "period_nm": p, "bandgap_meV": eg})
    return {"count": len(rows), "samples": rows}


@app.get("/benchmark/moire")
def benchmark_moire() -> dict:
    work = Workload("ResNet-50 (INT8)", 4.0)
    modes = {}
    for mode in ("physics_target", "conservative"):
        assump = mode_assumptions(mode)
        modes[mode] = {
            "assumption": assump.note,
            "configs": moire_summary(work, mode),
        }
    return {"tile_configs": moire_configs(), "modes": modes}


@app.get("/benchmark/reference")
def benchmark_ref() -> dict:
    return {
        "platforms": [
            {"name": p.name, "tops": p.tops, "tops_per_w": p.tops_per_w, "power_w": p.power_w}
            for p in reference_platforms()
        ]
    }
