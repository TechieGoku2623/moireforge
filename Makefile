# Makefile for Moiré Superlattice SoC Design
# Supports simulation, synthesis, and documentation generation

.PHONY: all sim verilog python test solutions clean help diagrams benchmark next reproduce

# Default target
all: python solutions

# Python simulations
python:
	@echo "Running Python physics simulations..."
	python -m sim.moire_physics
	python -m sim.moire_logic_cell
	python -m sim.performance_benchmark

# Solution tests
solutions:
	@echo "Testing solutions..."
	python solutions/twist_angle_calibration.py
	python solutions/temperature_management.py
	python solutions/yield_optimization.py
	python solutions/integration_flow.py

# Run all tests
test:
	@echo "Running comprehensive test suite..."
	python scripts/run_all_tests.py

# Verilog simulation (requires Icarus Verilog or similar)
SIMULATOR ?= iverilog

verilog: rtl/tb_moire_gates.v
	@echo "Compiling Verilog testbench..."
	$(SIMULATOR) -o moire_gates_tb rtl/tb_moire_gates.v rtl/moire_cell.v rtl/moire_gates.v
	@echo "Running simulation..."
	vvp moire_gates_tb
	@echo "View waveform: gtkwave moire_gates.vcd"

# Run all simulations
sim: python solutions verilog

# Generate diagrams
diagrams:
	@echo "Generating architecture diagrams..."
	python scripts/generate_diagrams.py

benchmark:
	python scripts/run_benchmark_report.py

next:
	python scripts/run_next_step.py

reproduce:
	python scripts/reproduce.py

# Clean generated files
clean:
	rm -f *.vcd *.vvp moire_gates_tb
	rm -f *.png *.pdf
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Help target
help:
	@echo "Moiré Superlattice SoC Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  all        - Run all simulations and solutions"
	@echo "  python     - Run Python physics and performance simulations"
	@echo "  solutions  - Test all solution implementations"
	@echo "  test       - Run comprehensive test suite"
	@echo "  verilog    - Compile and run Verilog testbench"
	@echo "  sim        - Run all simulations (Python + Verilog)"
	@echo "  diagrams   - Generate architecture diagrams"
	@echo "  benchmark  - Write results/benchmark_report.txt"
	@echo "  next       - Next-step validation (yield + benchmark)"
	@echo "  reproduce  - Full Python reproducibility run + results/manifest.json"
	@echo "  clean      - Remove generated files"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  SIMULATOR  - Verilog simulator to use (default: iverilog)"
