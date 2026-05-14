export function About() {
  return (
    <div className="max-w-3xl space-y-4 text-sm leading-relaxed text-slate-700">
      <h1 className="text-2xl font-semibold text-slate-950">About</h1>
      <p>
        Stress Detection System (ECG / HRV) is an academic portfolio implementation focused on reproducible engineering:
        typed Python services, structured logging, containerized deployment, and a TypeScript dashboard for operational
        visibility.
      </p>
      <p>
        The dataset policy is strict: only WESAD chest ECG is used, with binary stress classification and no
        multimodal fusion. The UI communicates with versioned FastAPI routes under <code className="text-brand-500">/api/v1</code>.
      </p>
    </div>
  );
}
