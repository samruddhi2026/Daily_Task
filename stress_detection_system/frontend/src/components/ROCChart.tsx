import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type Pt = { x: number; y: number };

export function ROCChart({ fpr, tpr }: { fpr: number[]; tpr: number[] }) {
  const data: Pt[] = fpr.map((x, i) => ({ x, y: tpr[i] ?? 0 }));
  return (
    <div className="h-72 w-full rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
          <XAxis dataKey="x" name="FPR" stroke="#64748b" />
          <YAxis dataKey="y" name="TPR" stroke="#64748b" />
          <Tooltip contentStyle={{ background: "#ffffff", border: "1px solid #cbd5e1", color: "#0f172a" }} />
          <Line type="monotone" dataKey="y" stroke="#22c55e" dot={false} strokeWidth={1.5} isAnimationActive={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
