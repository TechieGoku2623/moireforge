<div align="center">

# MoiréForge

**A runnable planning stack for Moiré-superlattice edge AI**

Explore a twist-angle compute idea without pretending the silicon already exists. Physics envelopes, system-power benchmarks, yield tools, behavioral RTL, an API, and a live dashboard — with an evidence tier on every number.

[![Python](https://img.shields.io/badge/Python-sim%20%2B%20API-3776AB?logo=python&logoColor=white)](#quick-start)
[![Next.js](https://img.shields.io/badge/Dashboard-Next.js-000000?logo=nextdotjs)](#quick-start)
[![Evidence](https://img.shields.io/badge/Evidence-model--derived-CA8A04)](docs/EVIDENCE_TIERS.md)
[![Demo](https://img.shields.io/badge/Demo-plays%20on%20this%20page-38BDF8)](#watch-the-demo)

</div>

---

## The problem

Edge AI wants more TOPS/W than bulk CMOS is giving. Moiré materials are interesting because a **small twist** between 2D layers creates a large superlattice — in principle a tunable gap and a new accelerator tile.

The failure mode in this space is not “no ideas.” It is **unreproducible claims**: datasheet TOPS, missing system power, RTL that does not exist, and dashboards that cannot be traced to a script. A planner, investor, or researcher cannot tell model output from measured silicon.

## What this software does

MoiréForge turns the twist-angle sentence into something you can **run**:

```text
Twist angle  →  Moiré period  →  Bandgap envelope (with uncertainty)
             →  Logic-cell abstraction
             →  Tile count × power (accelerator + CPU / NoC / SRAM / DRAM / leakage)
             →  Yield under defects  +  thermal / calibration tools
             →  FastAPI  +  Next.js dashboard
```

**Conservative mode is the planning default.** System overhead is included so a “good looking” accelerator TOPS/W is not mistaken for a full SoC.

> Reported TOPS / TOPS/W are **model-derived**, not measured silicon. See [Evidence tiers](docs/EVIDENCE_TIERS.md).

---

## Watch the demo

The walkthrough **plays on this page**. It is the Next.js dashboard (`frontend/`) calling FastAPI (`saas/api/`).

<p align="center">
  <img src="docs/demo.gif" alt="MoiréForge dashboard walkthrough — plays inline" width="920"/>
</p>

| In the clip | Why it matters |
| --- | --- |
| KPIs | API health, evidence = **model**, system TOPS/W |
| Repository alignment | Dashboard names folders that exist at repo root |
| Benchmarks | Small / medium / large tiles with system overhead |
| Physics sweep | Twist ° → period nm → bandgap meV from the same `sim/` model |

---

## How it is organized

| Area | What you can execute |
| --- | --- |
| Physics | `sim/` — twist → period → bandgap envelope |
| Performance | Target vs conservative benchmarks |
| Yield / thermal | Monte Carlo and throttle helpers in `solutions/` |
| Hardware path | Behavioral Verilog stubs in `rtl/` (CPU, tiles, NoC, PMU) |
| Product surface | FastAPI + Next.js dashboard |
| Reproducibility | `python scripts/reproduce.py` |

| Evidence tier | Meaning |
| --- | --- |
| **1 – Executable** | Sims, tests, figures, manifest |
| **2 – Prototype** | Behavioral RTL / firmware / EDA stubs |
| **3 – Future** | Measured silicon, PDK signoff |

```text
moireforge/
├── sim/                 Physics, logic cells, benchmarks
├── solutions/           Calibration, yield, thermal
├── rtl/                 Behavioral Verilog stubs
├── saas/api/            FastAPI
├── frontend/            Next.js dashboard (demo UI)
├── scripts/             reproduce, diagrams
├── tests/
├── docs/                Evidence, architecture, methods
├── config/              Physics + system overhead
└── requirements.txt
```

Details: [SoC architecture](docs/SOC_ARCHITECTURE.md) · [Limitations](docs/LIMITATIONS_AND_RESOLUTION_PLAN.md) · [Literature](docs/LITERATURE_VALIDATION.md)

---

## Quick start

```bash
pip install -r requirements.txt
python scripts/reproduce.py
```

Step by step:

```bash
python -m sim.moire_physics
python -m sim.moire_logic_cell
python -m sim.performance_benchmark
python -m pytest tests -q
```

**API + dashboard**

```bash
python -m uvicorn saas.api.main:app --host 127.0.0.1 --port 8000
cd frontend && npm install && npm run dev    # http://localhost:3000
```

Windows: `.\run.ps1 api` and `.\run.ps1 web`. Optional `NEXT_PUBLIC_API_URL`. Optional `make verilog` if Icarus Verilog is installed.

---

<p align="center"><sub>MoiréForge · if a number cannot be reproduced from sim/ + config/, it does not belong on the dashboard</sub></p>
