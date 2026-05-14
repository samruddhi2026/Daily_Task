import { Link } from "react-router-dom";

export function Navbar() {
  return (
    <header className="border-b border-slate-200 bg-white/90 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <div className="text-sm font-semibold tracking-wide text-slate-900">
          Stress Detection <span className="text-brand-600">ECG / HRV</span>
        </div>
        <Link
          to="/"
          className="text-xs font-medium text-slate-600 underline-offset-4 hover:text-brand-600 hover:underline"
        >
          Back to home
        </Link>
      </div>
    </header>
  );
}
