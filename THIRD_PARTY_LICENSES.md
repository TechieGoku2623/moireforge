# Third-Party Code and Licenses

This project lists any third-party code here with **copyright**, **license**, and **source** so there is no misappropriation and no one is unintentionally implicated in legal proceedings.

---

## No third-party RTL included

The repository **does not include any third-party RTL**. The RISC-V CPU is our **in-house minimal RV32I core** in **`rtl/riscv_cpu_core.v`**. Build and use require no external CPU code.

---

## If you add optional third-party code

### PicoRV32 (optional, external – not in repo)

If you download and add PicoRV32 yourself (e.g. into `rtl/cores/picorv32/`), keep this attribution:

| Item | Details |
|------|--------|
| **Copyright** | (C) 2015 Claire Xenia Wolf <claire@yosyshq.com> |
| **License** | **ISC** (use, copy, modify, distribute; keep copyright and permission notice; no warranty). |
| **Source** | https://github.com/YosysHQ/picorv32 |

See `rtl/cores/picorv32/README.md` and `docs/RISCV_INTEGRATION_GUIDE.md` for optional integration.

---

## Policy

- **No proprietary or non‑permissively licensed code** is intentionally included without explicit permission and documentation here.
- **All third-party components** used in this repository are listed in this file with copyright, license, and source.
- If you add or remove third-party code, update this file and keep the project in compliance with each component’s license.

For general legal and IP (patents, publication), see `docs/PATENT_CLAIMS.md` and `docs/DATA_AND_CODE_AVAILABILITY.md`.
