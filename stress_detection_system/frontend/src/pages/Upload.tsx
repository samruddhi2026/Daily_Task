import { useMemo, useState } from "react";
import { Loader } from "../components/Loader";
import type { Prediction } from "../types/prediction";
import { SignalChart } from "../components/SignalChart";
import { Toast } from "../components/Toast";
import { UploadCard } from "../components/UploadCard";
import { PredictionCard } from "../components/PredictionCard";
import { uploadCsv } from "../services/api";
import { getApiErrorMessage } from "../utils/apiError";

export function Upload() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [ecg, setEcg] = useState<number[] | null>(null);
  const [fs, setFs] = useState(700);

  const chart = useMemo(() => {
    if (!ecg) return null;
    return <SignalChart ecg={ecg} fs={fs} />;
  }, [ecg, fs]);

  const onFile = async (file: File) => {
    setBusy(true);
    setError(null);
    setPrediction(null);
    setEcg(null);
    try {
      const text = await file.text();
      const lines = text.split(/\r?\n/).filter(Boolean);
      const header = lines[0].split(",").map((h) => h.trim().toLowerCase());
      const ecgIdx = header.findIndex((h) => ["ecg", "signal", "ecg_mv", "voltage"].includes(h));
      const col = ecgIdx >= 0 ? ecgIdx : 0;
      const vals: number[] = [];
      for (let i = 1; i < lines.length; i++) {
        const parts = lines[i].split(",");
        const v = Number(parts[col]);
        if (Number.isFinite(v)) vals.push(v);
      }
      setEcg(vals);
      const res = await uploadCsv(file, fs);
      setPrediction(res);
    } catch (e) {
      setError(getApiErrorMessage(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-950">Upload data</h1>
        <p className="mt-2 text-sm text-slate-600">
          Provide a CSV with an ECG column. Set the sampling rate to how often samples were recorded (not the model
          default unless it matches your file). The API needs at least <strong>60 seconds</strong> of samples at that
          rate (for example at 700&nbsp;Hz you need roughly 42,000 rows).
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        <label className="text-sm text-slate-800">
          Sampling rate (Hz)
          <input
            type="number"
            className="mt-2 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900"
            value={fs}
            min={20}
            max={2000}
            onChange={(e) => setFs(Number(e.target.value))}
          />
        </label>
      </div>
      <UploadCard onFile={onFile} busy={busy} />
      {busy ? <Loader label="Running inference pipeline…" /> : null}
      {error ? <Toast tone="error" message={error} /> : null}
      {chart}
      {prediction ? <PredictionCard data={prediction} /> : null}
    </div>
  );
}
