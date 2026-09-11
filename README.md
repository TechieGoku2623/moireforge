# MoiréForge

**Moiré Superlattice SoC framework for edge AI exploration**

MoiréForge is an open design-and-simulation stack for a hybrid **CMOS + Moiré accelerator** architecture. It includes runnable physics models, dual-mode performance benchmarks (with system power overhead), calibration/yield/thermal solutions, behavioral RTL stubs, a FastAPI service, and reproducibility tooling.

> **Important:** Reported TOPS / TOPS/W numbers are **model-derived**, not measured silicon. Prefer **conservative** mode for planning. See [Evidence tiers](docs/EVIDENCE_TIERS.md).

---

## Highlights

| Area | What you get |
|------|----------------|
| Physics | Twist → period → bandgap envelope, exciton/mobility heuristics |
| Performance | Target vs conservative modes + **system** power overhead |
| Yield / reliability | Redundancy MC, defect/marginal tiles, thermal throttle |
| Hardware path | Behavioral Verilog stubs (CPU, tiles, NoC, PMU) |
| Software | FastAPI, Next.js dashboard scaffold, Python SDK stub |
| Reproducibility | One-command `scripts/reproduce.py` + manifest |

---

## Quick start

```bash
pip install -r requirements.txt

# Full reproducible run (tests, sims, figures, report, manifest)
python scripts/reproduce.py

# Or step by step
python -m sim.moire_physics
python -m sim.moire_logic_cell
python -m sim.performance_benchmark
python -m pytest tests -q
```

**Windows (PowerShell):**

```powershell
.\run.ps1 test
.\run.ps1 diagrams
.\run.ps1 sim
.\run.ps1 reproduce
.\run.ps1 help
```

**API + dashboard (optional):**

```powershell
.\run.ps1 api    # http://127.0.0.1:8000
.\run.ps1 web    # http://localhost:3000  (requires Node.js)
```

**Verilog (optional, needs Icarus Verilog):**

```bash
make verilog
```

---

## Visual results

Regenerate anytime with `python scripts/generate_diagrams.py` or `.\run.ps1 diagrams`.

<p align="center">
  <img src="docs/generated/performance_comparison.png" alt="Performance comparison" width="900"/>
</p>

<p align="center"><sub>System TOPS/W includes CPU / NoC / SRAM / DRAM / leakage overhead — target vs conservative vs baselines</sub></p>

<p align="center">
  <img src="docs/generated/problem_solution_map.png" alt="Problem to solution map" width="900"/>
</p>

<p align="center"><sub>How this repo maps real edge-AI / integration pain points to executable tools</sub></p>

| Bandgap envelope | Yield under defects |
|:---:|:---:|
| ![Bandgap vs twist](docs/generated/bandgap_vs_twist.png) | ![Yield with defects](docs/generated/yield_with_defects.png) |

<p align="center">
  <img src="docs/generated/soc_block_diagram.png" alt="SoC block diagram" width="720"/>
</p>

<p align="center"><sub>Conceptual SoC block diagram (RTL is behavioral / stub-level today)</sub></p>

---

## Example model output

Workload: ResNet-50 INT8 · 4 GOp/inference · **Medium (16 tiles)** · `physics_target`

| Metric | Value |
|--------|------:|
| Throughput | 204.8 TOPS |
| Accelerator power | 8.0 W |
| System overhead | ~4.5 W |
| **System power** | **~12.5 W** |
| Accel efficiency | 25.6 TOPS/W |
| **System efficiency** | **~16.4 TOPS/W** |
| Latency | 19.5 ms |

Full tables: [Market comparison](docs/MARKET_COMPARISON.md)

---

## Repository map

```text
CHIP/
├── sim/                 # Physics, logic cells, benchmarks, literature anchors
├── solutions/           # Calibration, yield, temperature, integration
├── transport/           # Ballistic / tunneling helpers
├── digital_twin/        # Aging / defect-rate stubs
├── rtl/                 # Behavioral Verilog (CPU, tiles, NoC, PMU)
├── firmware/            # Boot + driver stubs
├── software/            # Python SDK stub
├── eda/                 # Synthesis / P&R script stubs
├── saas/                # FastAPI (physics, benchmark, yield)
├── frontend/            # Next.js dashboard scaffold
├── scripts/             # reproduce, diagrams, market table, RTL lint
├── tests/               # pytest suite
├── docs/                # Architecture, evidence, literature, methods
├── config/              # calibration.json (physics + system overhead)
├── requirements.txt
├── run.ps1 / run.bat
└── Makefile
```

---

## Architecture (short)

- **Control:** minimal in-house RV32I stub (`rtl/riscv_cpu_core.v`)
- **Compute:** Moiré accelerator tiles (4–64 in the model)
- **Fabric:** mesh NoC stub, hybrid memory story, PMU/DVFS hooks
- **Flow:** physics → logic abstraction → RTL stubs → workload model

Details: [SoC architecture](docs/SOC_ARCHITECTURE.md)

---

## Evidence & honesty

| Tier | Meaning |
|------|---------|
| **1 – Executable** | Sims, solutions, tests, figures, `results/manifest.json` |
| **2 – Prototype** | Behavioral RTL / firmware / EDA stubs |
| **3 – Future** | Measured silicon, PDK signoff, production runtime |

- [Evidence tiers](docs/EVIDENCE_TIERS.md)
- [Limitations & resolution plan](docs/LIMITATIONS_AND_RESOLUTION_PLAN.md)
- [Literature validation](docs/LITERATURE_VALIDATION.md)
- [Methods snapshot](docs/METHODS_SNAPSHOT.md)
- [Reproduce guide](REPRODUCE.md)

---

## Docs & legal

| Doc | Purpose |
|-----|---------|
| [QUICK_START.md](QUICK_START.md) | Short command cheat sheet |
| [REPRODUCE.md](REPRODUCE.md) | Clean-machine reproduction |
| [LEGAL.md](LEGAL.md) | Attribution policy |
| [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) | Third-party notices |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |

---

## License

Research and educational use. See project legal docs for attribution policy.

---

**MoireQuantum Edge Processor** · Last updated 2026-09-10
