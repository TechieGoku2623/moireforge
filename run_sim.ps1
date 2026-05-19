# Run simulations (replaces: make sim)
Write-Host "Running Python physics simulation..." -ForegroundColor Cyan
python -m sim.moire_physics
Write-Host "`nRunning logic cell simulation..." -ForegroundColor Cyan
python -m sim.moire_logic_cell
Write-Host "`nTesting solutions..." -ForegroundColor Cyan
python solutions/twist_angle_calibration.py
python solutions/temperature_management.py
python solutions/yield_optimization.py
python solutions/integration_flow.py
Write-Host "`nDone." -ForegroundColor Green
