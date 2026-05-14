import { NavLink, Outlet } from "react-router-dom";
import { Navbar } from "../components/Navbar";
import { Sidebar } from "../components/Sidebar";

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `block rounded-md px-3 py-2 text-sm ${isActive ? "bg-slate-200 text-brand-600" : "text-slate-700 hover:bg-slate-100"}`;

export function DashboardLayout() {
  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-950">
      <Sidebar>
        <NavLink to="/dashboard" className={linkClass}>
          Dashboard
        </NavLink>
        <NavLink to="/upload" className={linkClass}>
          Upload Data
        </NavLink>
        <NavLink to="/metrics" className={linkClass}>
          Model Metrics
        </NavLink>
        <NavLink to="/insights" className={linkClass}>
          Research Insights
        </NavLink>
        <NavLink to="/about" className={linkClass}>
          About
        </NavLink>
      </Sidebar>
      <div className="flex min-w-0 flex-1 flex-col">
        <Navbar />
        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
