# Run all tests (replaces: make test)
Write-Host "Running comprehensive test suite..." -ForegroundColor Cyan
python scripts/run_all_tests.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "`nRunning unit tests..." -ForegroundColor Cyan
python -m pytest tests/ -v --tb=short
exit $LASTEXITCODE
