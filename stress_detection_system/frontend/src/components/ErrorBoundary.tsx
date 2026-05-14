import { Component, type ErrorInfo, type ReactNode } from "react";

type Props = { children: ReactNode };

type State = { hasError: boolean; message?: string };

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, message: error.message };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("UI error boundary", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-slate-50 p-6 text-slate-950">
          <div className="max-w-lg rounded-xl border border-red-500/40 bg-white p-6 shadow-sm">
            <h1 className="text-lg font-semibold text-red-600">Something went wrong</h1>
            <p className="mt-2 text-sm text-slate-700">{this.state.message}</p>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
