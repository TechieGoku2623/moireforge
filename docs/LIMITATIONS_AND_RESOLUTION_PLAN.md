# Limitations and Resolution Plan

This document tracks known gaps and concrete actions to close them.

## 1) Physics model confidence

### Current limitation
- `sim/moire_physics.py` uses phenomenological relationships.
- Parameters are configurable, but not tied to a published calibration dataset yet.

### Resolution
- Add literature-backed validation ranges and citations.
- Add dataset-driven calibration input file(s) with provenance.
- Report error envelopes (best/typical/worst) next to nominal curves.

## 2) Benchmark credibility

### Current limitation
- Performance is model-derived and sensitive to assumptions.
- Baseline rows are simplified, not full system reproductions.

### Resolution
- Keep two explicit modes: `physics_target` and `conservative`.
- Add workload/memory accounting sheet and publish assumptions.
- Add benchmark sanity tests to prevent accidental drift.

## 3) RTL maturity

### Current limitation
- Major blocks in `rtl/` are architecture-level stubs.
- No full production verification matrix yet.

### Resolution
- Add lint + simulation regression in CI for RTL blocks.
- Incrementally replace stubs with validated implementation modules.
- Track coverage and property checks per RTL block.

## 4) Software/API production readiness

### Current limitation
- API is designed for local research workflows and demos.
- Security/ops controls (auth, quotas, telemetry) are minimal.

### Resolution
- Introduce auth and rate-limits for hosted deployments.
- Add structured logs, health SLOs, and deployment runbooks.
- Separate demo mode from production mode in configuration.

## 5) Reproducibility scope

### Current limitation
- Reproducibility is strong for Python model stack, weaker for full hardware flow.

### Resolution
- Continue publishing `results/manifest.json` from CI artifacts.
- Add optional environment lockfile for stricter reproducibility.
- Expand reproduce script with optional RTL/EDA stage gates when tools exist.

