# Reproducibility Guide
## MoireQuantum Edge Processor — Step-by-Step

This guide gives **minimal steps** to reproduce the main results (performance benchmarks, market comparison, yield and calibration) on a clean machine. For full methods and limitations, see **docs/NATURE_METHODS_AND_REPRODUCIBILITY.md** and **docs/DATA_AND_CODE_AVAILABILITY.md**.

---

## Prerequisites

- **Python:** 3.10 or higher  
- **Optional:** Verilog simulator (e.g. Icarus Verilog) for RTL; not required for benchmarks or yield.

---

## 1. Clone and install

```bash
# Clone the repository (or unpack the release tarball)
cd /path/to/CHIP

# Create a virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Performance benchmark (physics target + conservative)

Generates the main efficiency numbers and writes a report to `results/benchmark_report.txt`.

**Windows (PowerShell):**
```powershell
.\run.ps1 benchmark
```
Or run the report script directly:
```powershell
python scripts/run_benchmark_report.py
```

**Linux/macOS:**
```bash
make benchmark
# or
python scripts/run_benchmark_report.py
```

**What you get:**  
- Throughput (TOPS), accelerator and **system** power, **system TOPS/W** for Small/Medium/Large configs.  
- Each config reported in **two modes:** **physics target** (market-leading, ~25–100 TOPS/W) and **conservative** (~2 TOPS/W).  
- Baseline platforms (ARM A78, NVIDIA A100, Google TPU, Intel Loihi 2).

---

## 3. Yield and defect simulation

Runs yield optimization with defect injection (e.g. 15% defective, 10% marginal) and prints a short benchmark summary.

**Windows (PowerShell):**
```powershell
.\run.ps1 next
```

**Linux/macOS:**
```bash
make next
# or
python scripts/run_next_step.py
```

**What you get:**  
- Number of logical tiles still operational with redundancy.  
- Summary of benchmark (physics + conservative) for the configured tile count.

---

## 4. Calibration simulation

Runs the twist-angle / electrical calibration model (post-fabrication offset extraction).

```bash
python solutions/twist_angle_calibration.py
```

---

## 5. Full test suite

Runs all project tests (physics, logic cells, performance model, solutions, etc.).

**Windows (PowerShell):**
```powershell
.\run.ps1 test
```

**Linux/macOS:**
```bash
python -m pytest tests/ -v
# or
make test
```

**What you get:**  
- Pass/fail for each test; any failure should be resolved before citing reproducibility.

---

## 6. Market comparison table

The table in **docs/MARKET_COMPARISON.md** is produced from the same performance model and baselines. After running step 2, the numbers in the report match the model; the markdown table can be updated from those results or by re-running the benchmark script.

---

## 7. RTL simulation (optional)

If you have a Verilog simulator (e.g. Icarus Verilog):

```bash
# From project root; exact command may depend on your Makefile/setup
cd rtl
iverilog -o tb_moire_gates.vvp -s tb_moire_gates tb_moire_gates.v moire_gates.v moire_cell.v
vvp tb_moire_gates.vvp
```

---

## Quick one-liner (Python only — recommended)

From the repo root after `pip install -r requirements.txt`:

```bash
python scripts/reproduce.py
```

This runs the full test suite, all simulation modules, solution scripts, diagram generation, the benchmark report writer, and writes **`results/manifest.json`** (Python version, platform, git commit, key package versions).

For benchmarks + next-step yield only (no full suite):

```bash
python scripts/run_benchmark_report.py
python scripts/run_next_step.py
python -m pytest tests/ -v
```

**Windows:** `.\run.ps1 reproduce` or `run.bat reproduce` (sets UTF-8 for console output).

---

## Output locations

| Output | Location |
|--------|----------|
| Benchmark report | `results/benchmark_report.txt` |
| Reproduce manifest | `results/manifest.json` |
| Performance comparison figure | `docs/generated/performance_comparison.png` |
| Problem → solution map | `docs/generated/problem_solution_map.png` |
| Bandgap / SoC figures | `docs/generated/bandgap_vs_twist.png`, `docs/generated/soc_block_diagram.png` |
| Market comparison text | `docs/MARKET_COMPARISON.md` |

---

## Troubleshooting

- **ModuleNotFoundError:** Run from the project root so that `sim`, `solutions`, and `scripts` are on the path, or use `python -m` as in the test command.  
- **Unicode/Windows:** If the console errors on special characters, run with `PYTHONIOENCODING=utf-8` or use the scripts that avoid non-ASCII in print.  
- **Tests fail:** Ensure `requirements.txt` is installed and you have run from the repo root; see **docs/NATURE_METHODS_AND_REPRODUCIBILITY.md** for limitations and contact info.

---

## Citation and code availability

When citing reproducibility, point to this repository and to:

- **Methods and limitations:** `docs/NATURE_METHODS_AND_REPRODUCIBILITY.md`  
- **Data and code availability:** `docs/DATA_AND_CODE_AVAILABILITY.md`  
- **Recommendations and suggestions:** `docs/RECOMMENDATIONS_AND_SUGGESTIONS.md`

---

**Document version:** 1.0
