import { Component, type ErrorInfo, type ReactNode } from "react";

interface WorldCanvasBoundaryProps {
  children: ReactNode;
  fallback: ReactNode;
}

interface WorldCanvasBoundaryState {
  failed: boolean;
}

export class WorldCanvasBoundary extends Component<
  WorldCanvasBoundaryProps,
  WorldCanvasBoundaryState
> {
  state: WorldCanvasBoundaryState = { failed: false };

  static getDerivedStateFromError(): WorldCanvasBoundaryState {
    return { failed: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Portfolio world renderer failed.", error, info.componentStack);
  }

  render() {
    if (this.state.failed) return this.props.fallback;
    return this.props.children;
  }
}
