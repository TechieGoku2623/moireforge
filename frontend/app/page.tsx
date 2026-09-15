"use client";

import { useEffect, useMemo, useState } from "react";

const API = (process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");

const STRUCTURE = [
  { path: "sim/", role: "Physics, cells, benchmarks" },
  { path: "solutions/", role: "Yield, calibration, thermal" },
  { path: "rtl/", role: "Behavioral Verilog stubs" },
  { path: "saas/api/", role: "FastAPI: health, sweep, yield" },
  { path: "frontend/", role: "This dashboard" },
  { path: "docs/", role: "Evidence, architecture, figures" },
];

type Health = { ok?: boolean; service?: string; evidence_tier?: string; error?: string };
type BenchRow = { system_tops_per_w?: number; latency_ms?: number; tops?: number };
type Bench = {
  modes?: Record<string, { assumption?: string; configs?: Record<string, BenchRow> }>;
  error?: string;
};
type Sweep = { samples?: Array<{ twist_deg: number; period_nm: number; bandgap_meV: number }>; error?: string };

async function loadJson<T>(url: string, init?: RequestInit): Promise<T | { error: string }> {
  try {
    const response = await fetch(url, { cache: "no-store", ...init });
    if (!response.ok) return { error: `HTTP ${response.status}` };
    return (await response.json()) as T;
  } catch (error) {
    return { error: error instanceof Error ? error.message : "fetch failed" };
  }
}

export default function Page() {
  const [health, setHealth] = useState<Health>({});
  const [bench, setBench] = useState<Bench>({});
  const [sweep, setSweep] = useState<Sweep>({});

  useEffect(() => {
    loadJson<Health>(`${API}/health`).then(setHealth);
    loadJson<Bench>(`${API}/benchmark/moire`).then(setBench);
    loadJson<Sweep>(`${API}/physics/sweep`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ twist_start: 0.5, twist_end: 3, points: 8 }),
    }).then(setSweep);
  }, []);

  const conservative = bench.modes?.conservative?.configs ?? {};
  const headline = useMemo(() => {
    const medium = conservative["Medium"] ?? Object.values(conservative)[0];
    return medium?.system_tops_per_w;
  }, [conservative]);

  return (
    <main>
      <header className="hero">
        <p className="eyebrow">Moiré superlattice SoC</p>
        <h1>MoiréForge dashboard</h1>
        <p className="muted">
          Live view of physics sweep, model-derived efficiency, and the repository map this stack
          actually ships.
        </p>
      </header>

      <section className="kpis">
        <article className="panel">
          <span>API</span>
          <strong>{health.ok ? "Healthy" : health.error ?? "Offline"}</strong>
          <p className="muted">{health.service ?? "start uvicorn saas.api.main:app"}</p>
        </article>
        <article className="panel">
          <span>Evidence tier</span>
          <strong>{health.evidence_tier ?? "model"}</strong>
          <p className="muted">Not measured silicon — conservative planning mode</p>
        </article>
        <article className="panel">
          <span>System efficiency</span>
          <strong>{headline ? `${Number(headline).toFixed(1)} TOPS/W` : "—"}</strong>
          <p className="muted">Includes CPU / NoC / memory overhead</p>
        </article>
      </section>

      <section className="grid">
        <article className="panel">
          <h2>Repository alignment</h2>
          <ul className="tree">
            {STRUCTURE.map((row) => (
              <li key={row.path}>
                <code>{row.path}</code>
                <span>{row.role}</span>
              </li>
            ))}
          </ul>
        </article>
        <article className="panel">
          <h2>Benchmark configs</h2>
          {bench.error ? (
            <p className="muted">{bench.error}</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Config</th>
                  <th>TOPS/W</th>
                  <th>Latency</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(conservative).map(([name, row]) => (
                  <tr key={name}>
                    <td>{name}</td>
                    <td>{row.system_tops_per_w?.toFixed?.(1) ?? row.system_tops_per_w ?? "—"}</td>
                    <td>{row.latency_ms ? `${Number(row.latency_ms).toFixed(1)} ms` : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </article>
      </section>

      <article className="panel" style={{ marginTop: "1rem" }}>
        <h2>Physics sweep</h2>
        {sweep.error ? (
          <p className="muted">{sweep.error}</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Twist °</th>
                <th>Period nm</th>
                <th>Bandgap meV</th>
              </tr>
            </thead>
            <tbody>
              {(sweep.samples ?? []).map((sample) => (
                <tr key={sample.twist_deg}>
                  <td>{sample.twist_deg.toFixed(2)}</td>
                  <td>{sample.period_nm.toFixed(2)}</td>
                  <td>{sample.bandgap_meV.toFixed(1)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </article>
    </main>
  );
}
