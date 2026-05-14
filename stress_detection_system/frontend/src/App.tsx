import { Navigate, Route, Routes } from "react-router-dom";
import { DashboardLayout } from "./layouts/DashboardLayout";
import { About } from "./pages/About";
import { Dashboard } from "./pages/Dashboard";
import { Home } from "./pages/Home";
import { ModelMetrics } from "./pages/ModelMetrics";
import { ResearchInsights } from "./pages/ResearchInsights";
import { Upload } from "./pages/Upload";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route element={<DashboardLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/metrics" element={<ModelMetrics />} />
        <Route path="/insights" element={<ResearchInsights />} />
        <Route path="/about" element={<About />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
