import axios from "axios";

import type { Prediction } from "../types/prediction";

const api = axios.create({ baseURL: "/api/v1" });

export async function fetchMetrics(): Promise<unknown> {
  const { data } = await api.get("/metrics");
  return data;
}

export async function fetchModelInfo(): Promise<unknown> {
  const { data } = await api.get("/model/info");
  return data;
}

export async function trainModel(payload: { tune?: boolean; max_windows?: number | null }) {
  const { data } = await api.post("/train", payload);
  return data;
}

export async function uploadCsv(file: File, sampling_rate_hz: number): Promise<Prediction> {
  const fd = new FormData();
  fd.append("file", file);
  fd.append("sampling_rate_hz", String(sampling_rate_hz));
  const { data } = await api.post("/upload", fd);
  return data as Prediction;
}
