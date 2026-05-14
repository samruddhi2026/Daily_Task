import axios from "axios";

/** Extract a human-readable message from FastAPI / Axios errors. */
export function getApiErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err)) {
    const data = err.response?.data as { detail?: unknown; code?: string } | undefined;
    const detail = data?.detail;
    if (typeof detail === "string") {
      const code = typeof data?.code === "string" ? ` [${data.code}]` : "";
      return `${detail}${code}`;
    }
    if (Array.isArray(detail)) {
      return JSON.stringify(detail);
    }
    if (detail != null && typeof detail === "object") {
      return JSON.stringify(detail);
    }
    if (err.response?.status) {
      return `Request failed (${err.response.status})`;
    }
    return err.message;
  }
  if (err instanceof Error) return err.message;
  return "Request failed";
}
