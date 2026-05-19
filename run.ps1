# MoireQuantum Edge Processor - PowerShell runner
# Use: .\run.ps1 <target>
# Targets: test, sim, python, solutions, diagrams, all, clean, help

param(
    [Parameter(Position=0)]
    [string]$Target = "help"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Run-Test {
    Write-Host "Running comprehensive test suite..." -ForegroundColor Cyan
    python scripts/run_all_tests.py
}

function Run-Sim {
    Write-Host "Running Python simulations..." -ForegroundColor Cyan
    python -m sim.moire_physics
    python -m sim.moire_logic_cell
    python -m sim.performance_benchmark
    Write-Host "Running solution tests..." -ForegroundColor Cyan
    python solutions/twist_angle_calibration.py
    python solutions/temperature_management.py
    python solutions/yield_optimization.py
    python solutions/integration_flow.py
}

function Run-Python {
    Write-Host "Running Python physics simulations..." -ForegroundColor Cyan
    python -m sim.moire_physics
    python -m sim.moire_logic_cell
    python -m sim.performance_benchmark
}

function Run-Solutions {
    Write-Host "Testing solutions..." -ForegroundColor Cyan
    python solutions/twist_angle_calibration.py
    python solutions/temperature_management.py
    python solutions/yield_optimization.py
    python solutions/integration_flow.py
}

function Run-Diagrams {
    Write-Host "Generating architecture diagrams..." -ForegroundColor Cyan
    python scripts/generate_diagrams.py
}

function Run-NextStep {
    Write-Host "Running next-step validation (yield + benchmark)..." -ForegroundColor Cyan
    python scripts/run_next_step.py
}

function Run-BenchmarkReport {
    Write-Host "Running full benchmark report..." -ForegroundColor Cyan
    python scripts/run_benchmark_report.py
}

function Run-Pipeline {
    Write-Host "Running full pipeline (test + next + benchmark)..." -ForegroundColor Cyan
    python scripts/run_full_pipeline.py
}

function Run-Reproduce {
    Write-Host "Running full reproduce (tests, sims, diagrams, report, manifest)..." -ForegroundColor Cyan
    $env:PYTHONIOENCODING = "utf-8"
    python scripts/reproduce.py
}

function Run-Api {
    $port = 8000
    $inUse = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    if ($inUse) {
        $port = 8001
        Write-Host "Port 8000 is in use. Starting API on port $port instead." -ForegroundColor Yellow
        Write-Host "If using the frontend, set in frontend/.env.local: NEXT_PUBLIC_API_URL=http://127.0.0.1:$port" -ForegroundColor Gray
    }
    Write-Host "Starting Moire API (http://127.0.0.1:$port)..." -ForegroundColor Cyan
    Write-Host "Stop with Ctrl+C. Then run .\run.ps1 web in another terminal for the frontend." -ForegroundColor Gray
    python -m uvicorn saas.api.main:app --host 127.0.0.1 --port $port
}

function Run-Web {
    Write-Host "Starting frontend (http://localhost:3000)..." -ForegroundColor Cyan
    Write-Host "Ensure API is running first: .\run.ps1 api" -ForegroundColor Gray
    Set-Location frontend
    npm run dev
}

function Run-All {
    Run-Python
    Run-Solutions
    Run-Test
}

function Run-Clean {
    Write-Host "Cleaning generated files..." -ForegroundColor Cyan
    Remove-Item -Path "*.vcd", "*.vvp", "moire_gates_tb" -ErrorAction SilentlyContinue
    Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "Done." -ForegroundColor Green
}

function Show-Help {
    Write-Host @"

MoireQuantum Edge Processor - Commands
======================================

Usage: .\run.ps1 <target>

Targets:
  api       - Start SaaS API (port 8000). Run in one terminal.
  web       - Start frontend (port 3000). Run in another terminal after api.
  test      - Run comprehensive test suite
  sim       - Run all simulations (Python + solutions)
  python    - Run Python physics simulations only
  solutions - Test all solution implementations
  diagrams  - Generate architecture diagrams
  next      - Run next-step validation (yield + benchmark)
  benchmark - Full benchmark report -> results/benchmark_report.txt
  pipeline  - Full pipeline (test + next + benchmark)
  reproduce - Tests + all sims + solutions + diagrams + benchmark + results/manifest.json
  all       - Run python, solutions, and test
  clean     - Remove generated files
  help      - Show this message

Examples:
  .\run.ps1 test
  .\run.ps1 diagrams
  .\run.ps1 sim

"@ -ForegroundColor Yellow
}

switch ($Target.ToLower()) {
    "api"        { Run-Api }
    "web"        { Run-Web }
    "test"       { Run-Test }
    "sim"        { Run-Sim }
    "python"     { Run-Python }
    "solutions"  { Run-Solutions }
    "diagrams"   { Run-Diagrams }
    "next"       { Run-NextStep }
    "benchmark"  { Run-BenchmarkReport }
    "pipeline"   { Run-Pipeline }
    "reproduce"  { Run-Reproduce }
    "all"        { Run-All }
    "clean"      { Run-Clean }
    "help"       { Show-Help }
    default    {
        Write-Host "Unknown target: $Target" -ForegroundColor Red
        Show-Help
        exit 1
    }
}
