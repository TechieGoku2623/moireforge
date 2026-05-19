# MoiréForge
## Moiré Superlattice SoC — MoireQuantum Edge Processor

A complete digital design and simulation framework for a **Moiré Superlattice-Based System-on-Chip** optimized for edge AI inference. This repository reports **model-derived** performance envelopes (physics-target and conservative) and provides executable simulations, RTL stubs, calibration and yield workflows, and reproducibility tooling (see `docs/`).

**CPU:** Default RISC-V CPU is our **in-house minimal RV32I** in `rtl/riscv_cpu_core.v` (no third-party CPU RTL required). **Third-party code and legal:** Any optional or included third-party components are listed in **`THIRD_PARTY_LICENSES.md`**. See **`LEGAL.md`** for policy on attribution.

---

## 🎯 **Project Overview**

This repository contains:

- **Device Physics Models**: Python simulations for twisted 2D materials (graphene, MoS₂/WSe₂) and exciton-based logic cells
- **RTL Design**: Complete Verilog models for Moiré logic gates, accelerator tiles, and full SoC architecture
- **Performance Benchmarks**: AI workload simulations comparing Moiré SoC vs CMOS/GPU/TPU
- **Architecture Documentation**: Detailed SoC block diagrams and patent-ready technical descriptions

---

## 📁 **Repository Structure**

```
CHIP/
├── physics_engine/               # Production Moiré physics (band structure, DoS, TBG/TMD)
├── transport/                    # Quantum-aware transport (ballistic, tunneling)
├── sim/                          # Device physics + logic (bandgap, excitons, benchmarks)
├── ai_optimization/              # Surrogate models, Bayesian opt, PINNs
├── digital_twin/                 # Aging, yield, defect prediction
├── manufacturing/               # GDSII export, tape-out checklist, readiness pack
├── rtl/                          # Verilog RTL (SoC, tiles, CPU, NoC, PMU)
├── eda/                          # Synthesis, place & route
├── firmware/                     # RISC-V firmware
├── software/                     # SDK, compiler spec
├── solutions/                    # Calibration, yield, temperature, integration
├── saas/                         # Moiré-as-a-Service API (FastAPI)
├── frontend/                     # Next.js dashboard (3D lattice, band structure, SoC)
├── business/                     # Pitch, business plan, hiring, funding, valuation
├── legal_ip/                     # Patent strategy, foundry NDA outline
├── docs/                         # Architecture, roadmaps, manuscript, legal
├── requirements.txt
├── Makefile
└── README.md
```

**Company vision and full roadmap:** see **`docs/MASTER_COMPANY_PLAN.md`**.

---

## 🚀 **Quick Start**

### **1. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **2. Run Python Simulations**

```bash
# Physics model: bandgap vs twist angle
python -m sim.moire_physics

# Logic gate abstraction: Moiré NAND truth table
python -m sim.moire_logic_cell

# Performance benchmarks: AI workload comparison
python -m sim.performance_benchmark
```

### **3. Run Commands (Windows)**

On Windows, use the PowerShell or batch runner (no `make` required):

```powershell
.\run.ps1 test       # Run all tests
.\run.ps1 diagrams   # Generate architecture diagrams
.\run.ps1 sim        # Run all simulations
.\run.ps1 solutions  # Test solution implementations
.\run.ps1 help       # Show all commands
```

Or use `run.bat` with the same targets: `run.bat test`, `run.bat diagrams`, etc.

### **4. Run Verilog Simulation** (optional, requires Icarus Verilog)

```bash
make verilog
# Or manually:
iverilog -o moire_gates_tb rtl/tb_moire_gates.v rtl/moire_cell.v rtl/moire_gates.v
vvp moire_gates_tb
gtkwave moire_gates.vcd  # View waveforms
```

---

## 🔬 **Key Features**

### **Device Physics Model**
- **Moiré period** vs twist angle calculation
- **Tunable bandgap** via twist angle and vertical electric field
- **Exciton binding energy** and lifetime modeling
- **Carrier mobility** vs moiré coupling strength
- **Logic state** abstraction using excitonic conduction

### **Logic Gate Design**
- **Moiré NAND/NOR/NOT** gates using excitonic cells
- **Configurable multi-input** gates
- **Behavioral Verilog models** for RTL simulation

### **SoC Architecture**
- **RISC-V CPU core** (CMOS) for control
- **Moiré accelerator tile array** (4-64 tiles)
- **Network-on-Chip (NoC)** with XY routing
- **Hybrid memory hierarchy** (SRAM + Moiré cache)
- **Power management unit** with DVFS

### **Performance Targets**
- **Throughput**: 100-500 TOPS (Tera Operations Per Second)
- **Energy Efficiency**: 10-50 TOPS/W
- **Latency**: < 1 ms per inference (ResNet-50)
- **Power**: 2-10 W active, < 10 mW sleep

---

## 📊 **Performance Benchmarks**

The `performance_benchmark.py` script compares Moiré SoC against:

- **CMOS CPU** (ARM Cortex-A78)
- **GPU** (NVIDIA A100)
- **TPU** (Google TPU v4)
- **Neuromorphic** (Intel Loihi 2)

Example output:
```
Workload: ResNet-50 (INT8)
  Operations per inference: 4.00 GOp

Moiré SoC Configurations (physics_target):
  Medium (16 tiles):
    Throughput: 204.80 TOPS
    Energy Efficiency: 25.60 TOPS/W
    Latency: 19.53 ms
    Power: 8.00 W
```

---

## 🏗️ **Architecture Highlights**

### **Moiré Accelerator Tile**
- **64-1024 compute units** per tile
- **1-4 KB local SRAM** buffer
- **Reconfigurable logic fabric** (NAND/NOR/NOT)
- **Excitonic compute engine** for AI inference

### **Network-on-Chip**
- **Mesh-based XY routing**
- **64-bit data width**, 32-bit address width
- **Address-based routing** to tiles and external memory

### **Memory Hierarchy**
1. L1 Cache (CPU): 32 KB I + 32 KB D
2. L2 Cache: 256 KB shared
3. Tile Local SRAM: 1-4 KB per tile
4. Moiré Cache: Excitonic memory (ultra-low-power)
5. External Memory: HBM2e/HBM3

---

## 🔧 **Design Methodology**

1. **Physics Modeling**: Python simulations for device behavior
2. **Logic Abstraction**: Python classes → Verilog behavioral models
3. **RTL Design**: Verilog modules for all functional blocks
4. **Performance Simulation**: AI workload benchmarking
5. **Architecture Documentation**: Patent-ready technical descriptions

---

## 📝 **Next Steps**

- [ ] **Physical Design**: Place & route, timing closure
- [ ] **Firmware**: RISC-V bootloader, Moiré ISA extensions
- [ ] **Compiler**: LLVM backend for Moiré instructions
- [ ] **Runtime**: Task scheduler, power-aware scheduling
- [ ] **SDK**: Python SDK for AI model deployment

---

## ⚠️ **Evidence Tiers & Limitations**

- **Tier 1 (implemented + reproducible):** executable simulations, solution scripts, test suite, generated figures, and `results/manifest.json` from `scripts/reproduce.py`.
- **Tier 2 (architectural prototypes):** RTL modules are primarily behavioral/stub-level for architecture exploration and API integration.
- **Tier 3 (future validation):** measured silicon data, PDK-closed timing/power, and full production firmware/runtime are not yet included.

See:
- **[Evidence tiers](docs/EVIDENCE_TIERS.md)**
- **[Limitations and resolution roadmap](docs/LIMITATIONS_AND_RESOLUTION_PLAN.md)**

---

## 📚 **Documentation**

- **[SoC Architecture](docs/SOC_ARCHITECTURE.md)**: Complete system specification
- **Code Comments**: Inline documentation in all modules
- **Performance Reports**: Generated by `performance_benchmark.py`
- **Result figures** (regenerate with `python scripts/generate_diagrams.py` or `.\run.ps1 diagrams`):
  - [Performance vs baselines](docs/generated/performance_comparison.png) — TOPS, TOPS/W, and latency from the same model as `sim.performance_benchmark` (illustrative; validate for your silicon and workload).
  - [Problems → what this repo provides](docs/generated/problem_solution_map.png) — maps edge-AI and integration pain points to simulations, RTL stubs, calibration, thermal/yield tools, and docs.
  - [Bandgap vs twist](docs/generated/bandgap_vs_twist.png) · [SoC blocks (conceptual)](docs/generated/soc_block_diagram.png)

### Visual Results

#### Performance Comparison (Target + Conservative vs Baselines)
![Performance comparison](docs/generated/performance_comparison.png)

#### Problem to Solution Mapping
![Problem solution map](docs/generated/problem_solution_map.png)

#### Bandgap vs Twist Angle
![Bandgap vs twist](docs/generated/bandgap_vs_twist.png)

#### SoC Conceptual Block Diagram
![SoC block diagram](docs/generated/soc_block_diagram.png)

---

## 🧪 **Testing**

```bash
# Run all tests
make sim

# Python only
make python

# Verilog only
make verilog

# Clean generated files
make clean
```

---

## 📄 **License**

This project is provided for research and educational purposes.

---

## 👥 **Contributors**

Designed and implemented as part of the **MoireQuantum Edge Processor** project.

---

**Last Updated**: 2026-02-05
