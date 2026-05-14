export function StressGauge({ confidence, label }: { confidence: number; label: string }) {
  const pct = Math.round(confidence * 100);
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="text-xs font-semibold uppercase tracking-widest text-slate-500">Model confidence</div>
      <div className="mt-4 text-3xl font-semibold text-slate-900">{pct}%</div>
      <div className="mt-2 text-sm text-slate-600">Outcome: {label}</div>
      <div className="mt-4 h-2 rounded-full bg-slate-200">
        <div className="h-2 rounded-full bg-brand-500" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
