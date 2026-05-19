# Generate diagrams (replaces: make diagrams)
Write-Host "Generating architecture diagrams..." -ForegroundColor Cyan
python scripts/generate_diagrams.py
Write-Host "`nDone. Check docs/ for generated images." -ForegroundColor Green
