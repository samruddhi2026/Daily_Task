import { useEffect } from "react";
import { Loader } from "../components/Loader";
import { MetricsPanel, type MetricsBundle } from "../components/MetricsPanel";
import { fetchMetrics } from "../services/api";
import { useAppStore } from "../store/useAppStore";

export function Dashboard() {
  const { metrics, setMetrics, error, setError } = useAppStore();

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const m = (await fetchMetrics()) as MetricsBundle;
        if (!cancelled) setMetrics(m);
      } catch (e) {
        if (!cancelled) setError("Metrics not available yet. Train the backend model first.");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [setError, setMetrics]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-950">Dashboard</h1>
        <p className="mt-2 text-sm text-slate-600">Latest evaluation artifacts from the training service.</p>
      </div>
      {error ? <div className="text-sm text-amber-300">{error}</div> : null}
      {!metrics && !error ? <Loader label="Loading metrics…" /> : null}
      {metrics ? <MetricsPanel metrics={metrics} /> : null}
    </div>
  );
}
