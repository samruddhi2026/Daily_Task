export function Loader({ label }: { label?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-10 text-slate-700">
      <div className="h-10 w-10 animate-spin rounded-full border-2 border-slate-200 border-t-brand-500" />
      {label ? <p className="text-sm">{label}</p> : null}
    </div>
  );
}
