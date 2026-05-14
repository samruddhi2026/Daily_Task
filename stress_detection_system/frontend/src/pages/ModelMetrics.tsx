import { useEffect, useState } from "react";
import { Loader } from "../components/Loader";
import { fetchModelInfo, trainModel } from "../services/api";

type ModelInfo = {
  artifacts_present: boolean;
  model_name?: string | null;
  feature_names?: string[] | null;
  best_model_path: string;
};

export function ModelMetrics() {
  const [info, setInfo] = useState<ModelInfo | null>(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = (await fetchModelInfo()) as ModelInfo;
        if (!cancelled) setInfo(data);
      } catch {
        if (!cancelled) setMsg("Could not reach the model info endpoint.");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const retrain = async () => {
    setBusy(true);
    setMsg(null);
    try {
      await trainModel({ tune: false });
      setMsg("Training finished. Refresh metrics pages to view updated artifacts.");
      setInfo((await fetchModelInfo()) as ModelInfo);
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Training failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold text-slate-950">Model metrics</h1>
          <p className="mt-2 text-sm text-slate-600">Inspect persisted artifacts and trigger retraining.</p>
        </div>
        <button
          type="button"
          onClick={retrain}
          disabled={busy}
          className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-brand-500 disabled:opacity-50"
        >
          {busy ? "Training…" : "Retrain models"}
        </button>
      </div>
      {msg ? <div className="text-sm text-amber-300">{msg}</div> : null}
      {!info && !msg ? <Loader label="Loading model metadata…" /> : null}
      {info ? (
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-xl border border-slate-200 bg-white p-4 text-sm shadow-sm">
            <div className="text-xs uppercase tracking-wide text-slate-500">Artifacts</div>
            <div className="mt-2 text-slate-900">{info.artifacts_present ? "Present on disk" : "Not trained yet"}</div>
            <div className="mt-3 text-xs text-slate-500">Best model</div>
            <div className="font-mono text-xs text-slate-700">{info.best_model_path}</div>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-4 text-sm shadow-sm">
            <div className="text-xs uppercase tracking-wide text-slate-500">Selected estimator</div>
            <div className="mt-2 text-lg font-semibold text-slate-950">{info.model_name ?? "—"}</div>
            <div className="mt-3 text-xs text-slate-500">Feature count</div>
            <div className="text-slate-700">{info.feature_names?.length ?? "—"}</div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
