# Evidence Tiers

This project intentionally separates executable evidence from aspirational claims.

## Tier 1: Executable and reproducible (current)

- Python simulations under `sim/`
- Solution modules under `solutions/`
- FastAPI endpoints under `saas/api/main.py`
- Tests under `tests/`
- Reproducibility run via `scripts/reproduce.py`
- Artifact manifest in `results/manifest.json`

Use this tier when making statements about what is currently demonstrated in code.

## Tier 2: Architectural prototypes (current)

- RTL hierarchy under `rtl/` is primarily behavioral/stub-level.
- Firmware and SDK contain integration scaffolding and placeholders.
- EDA scripts are flow stubs, not PDK-closed tape-out signoff scripts.

Use this tier when discussing implementation direction and integration strategy.

## Tier 3: Future validation (not yet in repository)

- Measured silicon performance/power data
- Closed-loop calibration from real wafers
- Full timing closure and signoff in foundry flow
- Production deployment hardening (auth, observability, quota, SLOs)

Use this tier only as roadmap language, not as validated outcomes.

