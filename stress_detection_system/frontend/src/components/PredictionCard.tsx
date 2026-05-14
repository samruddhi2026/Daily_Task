import type { Prediction } from "../types/prediction";
import { HRVFeatureTable } from "./HRVFeatureTable";
import { StressGauge } from "./StressGauge";

export function PredictionCard({ data }: { data: Prediction }) {
  return (
    <div className="space-y-4">
      {data.warnings?.length ? (
        <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-medium text-amber-900">
          {data.warnings[0]}
        </div>
      ) : null}
      <div className="grid gap-4 lg:grid-cols-3">
        <StressGauge confidence={data.confidence} label={data.prediction} />
        <div className="lg:col-span-2">
          <HRVFeatureTable features={data.features} />
        </div>
      </div>
    </div>
  );
}
