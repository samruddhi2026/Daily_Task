export function Toast({ message, tone = "info" }: { message: string; tone?: "info" | "error" }) {
  const cls =
    tone === "error"
      ? "border-red-500/40 bg-red-50 text-red-700"
      : "border-slate-200 bg-white text-slate-900";
  return (
    <div className={`rounded-lg border px-4 py-3 text-sm shadow-sm ${cls}`}>
      {message}
    </div>
  );
}
