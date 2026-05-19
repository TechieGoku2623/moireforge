async function fetchJson<T>(url: string): Promise<T | { error: string }> {
  try {
    const r = await fetch(url, { cache: "no-store" });
    if (!r.ok) return { error: `HTTP ${r.status}` };
    return (await r.json()) as T;
  } catch (e) {
    return { error: e instanceof Error ? e.message : "fetch failed" };
  }
}

const defaultApi = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default async function Page() {
  const base = defaultApi.replace(/\/$/, "");
  const health = await fetchJson<{ ok?: boolean; service?: string }>(`${base}/health`);
  const bench = await fetchJson<{ configs?: Record<string, unknown> }>(`${base}/benchmark/moire`);
  const latticeNote =
    "3D lattice / band visualization: use API `/physics/sweep` or run `python -m sim.moire_physics`.";

  return (
    <main>
      <h1>MoiréForge</h1>
      <p className="muted">
        Edge AI SoC dashboard. Start API: <code>.\run.ps1 api</code> then refresh.
      </p>

      <div className="grid">
        <div className="panel">
          <strong>API health</strong>
          <pre>{JSON.stringify(health, null, 2)}</pre>
        </div>
        <div className="panel">
          <strong>Benchmark configs</strong>
          <pre>{JSON.stringify(bench, null, 2)}</pre>
        </div>
      </div>

      <div className="panel" style={{ marginTop: "1rem" }}>
        <strong>Lattice &amp; bands</strong>
        <p className="muted" style={{ marginTop: "0.5rem" }}>
          {latticeNote} SoC diagram: <code>docs/generated/soc_block_diagram.png</code> from{" "}
          <code>.\run.ps1 diagrams</code>.
        </p>
      </div>

      <p className="muted" style={{ marginTop: "1.5rem" }}>
        Configure <code>NEXT_PUBLIC_API_URL</code> in <code>frontend/.env.local</code> if the API
        port differs (see run.ps1 api).
      </p>
    </main>
  );
}
