export function ResearchInsights() {
  return (
    <div className="max-w-3xl space-y-4 text-sm leading-relaxed text-slate-700">
      <h1 className="text-2xl font-semibold text-slate-950">Research insights</h1>
      <p className="mt-4">
        This system follows the WESAD protocol for chest-worn ECG at 700&nbsp;Hz. Labels are restricted to baseline
        (mapped to non-stress) and stress, excluding amusement, meditation, and undefined segments. Each analysis window
        enforces label purity so transitional segments are discarded.
      </p>
      <p className="mt-4">
        Heart rate variability is computed from beat-to-beat intervals after bandpass filtering and robust R-peak
        detection. Time-domain statistics capture autonomic modulation on short windows, frequency-domain summaries
        approximate sympathovagal balance, and nonlinear metrics summarize complexity and Poincaré structure.
      </p>
      <p className="mt-4">
        Models are compared on a held-out stratified split with ROC-AUC as the selection criterion, with optional
        randomized search for key estimators and a stacking ensemble as a strong non-linear baseline.
      </p>
    </div>
  );
}
