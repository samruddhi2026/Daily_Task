import { Link } from "react-router-dom";

export function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50 text-slate-950">
      <div className="mx-auto flex max-w-5xl flex-col gap-10 px-6 py-16">
        <header className="space-y-4">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-brand-600">Portfolio system</p>
          <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
            Stress detection from <span className="text-brand-600">ECG-derived HRV</span>
          </h1>
          <p className="max-w-2xl text-sm leading-relaxed text-slate-600">
            End-to-end pipeline on the WESAD dataset: chest ECG only, binary baseline versus stress, with preprocessing,
            R-peak detection, HRV features, classical and gradient-boosted models, and a deployable FastAPI service.
          </p>
        </header>
        <div className="flex flex-wrap gap-3">
          <Link
            to="/dashboard"
            className="rounded-lg bg-brand-600 px-5 py-2 text-sm font-semibold text-white hover:bg-brand-500"
          >
            Open dashboard
          </Link>
          <Link
            to="/upload"
            className="rounded-lg border border-slate-200 px-5 py-2 text-sm font-semibold text-slate-700 hover:border-brand-500/60"
          >
            Upload ECG CSV
          </Link>
        </div>
      </div>
    </div>
  );
}
