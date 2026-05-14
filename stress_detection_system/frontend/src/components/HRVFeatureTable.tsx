export function HRVFeatureTable({ features }: { features: Record<string, number> }) {
  const rows = Object.entries(features).sort(([a], [b]) => a.localeCompare(b));
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="w-full border-collapse text-left text-sm">
        <thead className="bg-slate-100 text-xs uppercase tracking-wide text-slate-500">
          <tr>
            <th className="px-4 py-3">Feature</th>
            <th className="px-4 py-3">Value</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([k, v]) => (
            <tr key={k} className="border-t border-slate-200 odd:bg-slate-50">
              <td className="px-4 py-2 font-mono text-xs text-slate-700">{k}</td>
              <td className="px-4 py-2 font-mono text-xs text-slate-900">{Number.isFinite(v) ? v.toFixed(4) : "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
