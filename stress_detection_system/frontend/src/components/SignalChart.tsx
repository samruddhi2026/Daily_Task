import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type Point = { t: number; v: number };

export function SignalChart({ ecg, fs }: { ecg: number[]; fs: number }) {
  const maxPts = 4000;
  const step = Math.max(1, Math.floor(ecg.length / maxPts));
  const data: Point[] = [];
  for (let i = 0; i < ecg.length; i += step) {
    data.push({ t: i / fs, v: ecg[i] ?? 0 });
  }

  return (
    <div className="h-72 w-full rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
          <XAxis dataKey="t" stroke="#64748b" fontSize={12} tickFormatter={(v) => `${v.toFixed(1)}s`} />
          <YAxis stroke="#64748b" fontSize={12} />
          <Tooltip
            contentStyle={{ background: "#ffffff", border: "1px solid #cbd5e1", color: "#0f172a" }}
            labelFormatter={(v) => `t = ${Number(v).toFixed(3)} s`}
          />
          <Line type="monotone" dataKey="v" stroke="#38bdf8" dot={false} strokeWidth={1.2} isAnimationActive={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
