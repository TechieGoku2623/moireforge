@echo off
REM MoireQuantum Edge Processor - Windows batch runner
REM Use: run.bat <target>
REM Targets: test, sim, python, solutions, diagrams, clean, help

setlocal
cd /d "%~dp0"

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="test" goto test
if "%1"=="sim" goto sim
if "%1"=="python" goto python
if "%1"=="solutions" goto solutions
if "%1"=="diagrams" goto diagrams
if "%1"=="next" goto next
if "%1"=="benchmark" goto benchmark
if "%1"=="pipeline" goto pipeline
if "%1"=="reproduce" goto reproduce
if "%1"=="clean" goto clean
echo Unknown target: %1
goto help

:test
echo Running comprehensive test suite...
python scripts/run_all_tests.py
goto end

:sim
echo Running Python simulations...
python -m sim.moire_physics
python -m sim.moire_logic_cell
echo Running solution tests...
python solutions/twist_angle_calibration.py
python solutions/temperature_management.py
python solutions/yield_optimization.py
python solutions/integration_flow.py
goto end

:python
echo Running Python physics simulations...
python -m sim.moire_physics
python -m sim.moire_logic_cell
goto end

:solutions
echo Testing solutions...
python solutions/twist_angle_calibration.py
python solutions/temperature_management.py
python solutions/yield_optimization.py
python solutions/integration_flow.py
goto end

:diagrams
echo Generating architecture diagrams...
python scripts/generate_diagrams.py
goto end

:next
echo Running next-step validation...
python scripts/run_next_step.py
goto end

:benchmark
echo Running full benchmark report...
python scripts/run_benchmark_report.py
goto end

:pipeline
echo Running full pipeline...
python scripts/run_full_pipeline.py
goto end

:reproduce
echo Running reproduce (UTF-8)...
set PYTHONIOENCODING=utf-8
python scripts/reproduce.py
goto end

:clean
echo Cleaning generated files...
del /q *.vcd *.vvp moire_gates_tb 2>nul
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
echo Done.
goto end

:help
echo.
echo MoireQuantum Edge Processor - Commands
echo ======================================
echo.
echo Usage: run.bat ^<target^>
echo.
echo Targets:
echo   test      - Run comprehensive test suite
echo   sim       - Run all simulations
echo   python    - Run Python physics simulations only
echo   solutions - Test all solution implementations
echo   diagrams  - Generate architecture diagrams
echo   next      - Run next-step validation (yield + benchmark)
echo   benchmark - Full benchmark report
echo   pipeline  - Full pipeline (test + next + benchmark)
echo   reproduce - Full Python reproducibility + manifest
echo   clean     - Remove generated files
echo   help      - Show this message
echo.
echo Examples:
echo   run.bat test
echo   run.bat diagrams
echo.
goto end

:end
endlocal
