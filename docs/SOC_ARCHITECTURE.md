# Moiré SoC Architecture (summary)

The hybrid SoC couples a **minimal RISC-V control core** with a **Moiré accelerator mesh**,
a **NoC**, hybrid memory, and **PMU** for DVFS-style throttling. RTL stubs live under `rtl/`.

See `README.md` for performance targets and repository map.
