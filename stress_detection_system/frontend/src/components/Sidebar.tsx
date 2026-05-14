import type { ReactNode } from "react";

export function Sidebar({ children }: { children: ReactNode }) {
  return (
    <aside className="hidden w-64 shrink-0 border-r border-slate-200 bg-white/90 p-4 md:block">
      <div className="mb-6 text-xs font-semibold uppercase tracking-widest text-slate-500">Navigation</div>
      <nav className="space-y-1">{children}</nav>
    </aside>
  );
}
