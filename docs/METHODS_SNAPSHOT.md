# Methods Snapshot (Model Framework)

## What is executable today

1. Phenomenological Moiré bandgap vs twist with configurable parameters (`config/calibration.json`).
2. Uncertainty envelope around the nominal gap (`bandgap_envelope_meV`).
3. Dual-mode SoC performance model: `physics_target` and `conservative`.
4. Yield Monte Carlo with binary die yield and three-state defects (good/marginal/defective).
5. Temperature throttle heuristics and integration checklist scripts.
6. Behavioral RTL stubs with explicit STUB markers; RTL lint via `scripts/lint_rtl.py`.

## Reproducibility

```bash
pip install -r requirements.txt
python scripts/reproduce.py
```

Artifacts: `results/benchmark_report.txt`, `results/manifest.json`, `docs/generated/*.png`.

## Limitations

See `docs/LIMITATIONS_AND_RESOLUTION_PLAN.md` and `docs/EVIDENCE_TIERS.md`.
This is a **design and simulation framework**, not a claim of measured silicon performance.
