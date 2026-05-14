import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type Row = { label: string; value: number };

export function ConfusionMatrixChart({ matrix, labels }: { matrix: number[][]; labels: string[] }) {
  const rows: Row[] = [];
  matrix.forEach((row, i) =>
    row.forEach((v, j) => {
      rows.push({ label: `${labels[i]} → pred ${j}`, value: v });
    })
  );

  return (
    <div className="h-72 w-full rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={rows}>
          <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
          <XAxis dataKey="label" stroke="#64748b" hide />
          <YAxis stroke="#64748b" />
          <Tooltip contentStyle={{ background: "#ffffff", border: "1px solid #cbd5e1", color: "#0f172a" }} />
          <Bar dataKey="value" fill="#38bdf8" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
