import type { ChangeEvent } from "react";

type Props = {
  onFile: (file: File) => void;
  busy?: boolean;
};

export function UploadCard({ onFile, busy }: Props) {
  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) onFile(f);
    e.target.value = "";
  };

  return (
    <label className="flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-slate-200 bg-white px-6 py-10 text-center shadow-sm transition hover:border-brand-500/60">
      <input type="file" accept=".csv,text/csv" className="hidden" onChange={onChange} disabled={busy} />
      <div className="text-sm font-medium text-slate-900">Drop or choose an ECG CSV</div>
      <div className="mt-2 text-xs text-slate-500">Include a column named ecg (or specify rate in the form).</div>
    </label>
  );
}
