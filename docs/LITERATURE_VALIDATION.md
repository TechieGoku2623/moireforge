# Literature Validation Anchors

> **Evidence tier:** citation-backed *motivation* for model form and ranges.  
> This is **not** a claim that the SoC TOPS/W numbers are experimentally measured.

Regenerate the table body from code:

```bash
python -c "from sim.literature import as_markdown_rows; print('\n'.join(as_markdown_rows()))"
```

## Citation table

| Key | Topic | How used in this repo | Reference (short) | Year |
|-----|-------|----------------------|-------------------|------|
| `tbg-magic-angle` | Twisted bilayer graphene magic angle | Sets magic_angle_deg ≈ 1.08 in config/calibration.json. | Cao et al., Nature (correlated insulating / superconducting TBG papers) | 2018 |
| `moire-period` | Moiré wavelength vs twist | Implements moire_period_nm() geometric relation. | Standard continuum moiré geometry (e.g. Lopes dos Santos / Bistritzer–MacDonald lineage) | 2007 |
| `tmd-excitons` | Excitons in 2D TMDs / moiré heterostructures | Motivates exciton_binding_meV() heuristic scaling with moiré period. | Reviews on TMD excitonics / moiré excitons (e.g. Wang, Mak, Shan lineage) | 2018 |
| `edge-efficiency` | Edge AI efficiency context | Motivates conservative vs physics_target dual reporting and system overhead model. | Industry edge-AI / MLPerf Tiny / mobile NPU efficiency discussions (contextual) | 2020 |
| `neuromorphic-efficiency` | Neuromorphic energy efficiency | Provides order-of-magnitude context for Loihi-class reference rows. | Intel Loihi / Loihi 2 technical reports and neuromorphic benchmarking literature | 2021 |

## Mapping to model knobs

| Model knob | File | Literature link |
|------------|------|-----------------|
| `magic_angle_deg` | `config/calibration.json` | `tbg-magic-angle` |
| `moire_period_nm` | `sim/moire_physics.py` | `moire-period` |
| `exciton_binding_meV` | `sim/moire_physics.py` | `tmd-excitons` |
| Dual efficiency modes + system power | `sim/performance_benchmark.py` | `edge-efficiency` |
| Neuromorphic reference row | `sim/performance_benchmark.py` | `neuromorphic-efficiency` |

## Uncertainty policy

- Physics curves use a configurable relative envelope (`literature_envelope.relative_uncertainty`).
- Performance reporting always shows **accelerator-only** and **system** TOPS/W after overheads.
- Prefer **conservative** mode for planning; treat **physics_target** as aspirational.

See also: `docs/EVIDENCE_TIERS.md`, `docs/LIMITATIONS_AND_RESOLUTION_PLAN.md`.
