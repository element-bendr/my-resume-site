import { describe, expect, it, vi } from "vitest";
import { hasUsableWebGLContext } from "../src/world/webgl";

describe("WebGL capability guard", () => {
  it("accepts WebGL2 when available", () => {
    const getContext = vi.fn((id: "webgl2" | "webgl") => (id === "webgl2" ? {} : null));
    expect(hasUsableWebGLContext(getContext)).toBe(true);
    expect(getContext).toHaveBeenCalledWith("webgl2");
  });

  it("falls back to WebGL1 when WebGL2 is unavailable", () => {
    const getContext = vi.fn((id: "webgl2" | "webgl") => (id === "webgl" ? {} : null));
    expect(hasUsableWebGLContext(getContext)).toBe(true);
  });

  it("fails closed when context creation throws", () => {
    expect(
      hasUsableWebGLContext(() => {
        throw new Error("GPU unavailable");
      }),
    ).toBe(false);
  });

  it("returns false when neither context is available", () => {
    expect(hasUsableWebGLContext(() => null)).toBe(false);
  });
});
