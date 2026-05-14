import { create } from "zustand";

import type { MetricsBundle } from "../components/MetricsPanel";

type State = {
  metrics: MetricsBundle | null;
  error: string | null;
  setMetrics: (m: MetricsBundle | null) => void;
  setError: (e: string | null) => void;
};

export const useAppStore = create<State>((set) => ({
  metrics: null,
  error: null,
  setMetrics: (m) => set({ metrics: m, error: null }),
  setError: (e) => set({ error: e }),
}));
