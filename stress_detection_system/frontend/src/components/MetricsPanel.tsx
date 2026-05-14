import { ConfusionMatrixChart } from "./ConfusionMatrixChart";
import { ROCChart } from "./ROCChart";

export type MetricsBundle = {
  test_metrics?: {
    accuracy?: number;
    precision?: number;
    recall?: number;
    f1?: number;
    roc_auc?: number;
    confusion_matrix?: { matrix: number[][]; labels: string[] };
    roc_curve?: { fpr: number[]; tpr: number[] };
  };
};

export function MetricsPanel({ metrics }: { metrics: MetricsBundle | null }) {
  if (!metrics?.test_metrics) {
    return <div className="text-sm text-slate-500">Train a model to populate evaluation charts.</div>;
  }
  const tm = metrics.test_metrics;
  const cards = [
    { k: "Accuracy", v: tm.accuracy },
    { k: "Precision", v: tm.precision },
    { k: "Recall", v: tm.recall },
    { k: "F1", v: tm.f1 },
    { k: "ROC-AUC", v: tm.roc_auc },
  ];
  return (
    <div className="space-y-6">
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
        {cards.map((c) => (
          <div key={c.k} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <div className="text-xs uppercase tracking-wide text-slate-500">{c.k}</div>
            <div className="mt-2 text-2xl font-semibold text-slate-900">
              {typeof c.v === "number" && Number.isFinite(c.v) ? c.v.toFixed(3) : "—"}
            </div>
          </div>
        ))}
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        {tm.confusion_matrix ? (
          <ConfusionMatrixChart matrix={tm.confusion_matrix.matrix} labels={tm.confusion_matrix.labels} />
        ) : null}
        {tm.roc_curve?.fpr && tm.roc_curve?.tpr ? (
          <ROCChart fpr={tm.roc_curve.fpr} tpr={tm.roc_curve.tpr} />
        ) : null}
      </div>
    </div>
  );
}
