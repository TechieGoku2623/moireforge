"""FastAPI app: health, physics sweep, benchmark, yield."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sim.moire_physics import bandgap_envelope_meV, bandgap_meV, moire_period_nm
from sim.performance_benchmark import mode_assumptions, moire_configs, moire_summary, reference_platforms, Workload
from solutions.yield_optimization import yield_with_defects

app = FastAPI(title="MoiréForge API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Health(BaseModel):
    ok: bool = True
    service: str = "moire-forge"
    evidence_tier: str = "model"


class SweepIn(BaseModel):
    twist_start: float = Field(0.5, ge=0.01, le=10)
    twist_end: float = Field(3.0, ge=0.01, le=10)
    points: int = Field(20, ge=3, le=200)


class DefectYieldIn(BaseModel):
    n_required: int = Field(16, ge=1, le=256)
    n_spare: int = Field(4, ge=0, le=256)
    p_defective: float = Field(0.15, ge=0.0, le=1.0)
    p_marginal: float = Field(0.10, ge=0.0, le=1.0)
    trials: int = Field(3000, ge=100, le=50_000)


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
        env = bandgap_envelope_meV(tw)
        rows.append(
            {
                "twist_deg": tw,
                "period_nm": p,
                "bandgap_meV": env.nominal_meV,
                "bandgap_low_meV": env.low_meV,
                "bandgap_high_meV": env.high_meV,
            }
        )
    return {"count": len(rows), "samples": rows, "note": bandgap_envelope_meV(1.08).note}


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


@app.post("/yield/defects")
def yield_defects(body: DefectYieldIn) -> dict:
    r = yield_with_defects(
        body.n_required,
        body.n_spare,
        p_defective=body.p_defective,
        p_marginal=body.p_marginal,
        trials=body.trials,
    )
    return {
        "p_system_ok": r.p_system_ok,
        "mean_good": r.mean_good,
        "mean_marginal": r.mean_marginal,
        "mean_defective": r.mean_defective,
        "trials": r.trials,
        "seed": r.seed,
    }
