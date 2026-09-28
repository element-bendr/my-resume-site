export type ContextGetter = (contextId: "webgl2" | "webgl") => unknown;

export function hasUsableWebGLContext(getContext: ContextGetter): boolean {
  try {
    return Boolean(getContext("webgl2") || getContext("webgl"));
  } catch {
    return false;
  }
}

export function detectWebGLSupport(): boolean {
  if (typeof document === "undefined") return false;

  const canvas = document.createElement("canvas");
  return hasUsableWebGLContext((contextId) =>
    canvas.getContext(contextId, {
      failIfMajorPerformanceCaveat: true,
      powerPreference: "high-performance",
    }),
  );
}
