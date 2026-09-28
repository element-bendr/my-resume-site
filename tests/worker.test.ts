import { describe, expect, it } from "vitest";
import worker from "../worker/index";

describe("portfolio Worker API", () => {
  it("returns a no-store health response", async () => {
    const response = worker.fetch(new Request("https://portfolio.example/api/health"));
    expect(response.status).toBe(200);
    expect(response.headers.get("cache-control")).toBe("no-store");
    await expect(response.json()).resolves.toEqual({
      ok: true,
      service: "vijay-kumaran-portfolio-world",
      stage: "app-foundation",
    });
  });

  it("returns structured 404s for unknown API routes", async () => {
    const response = worker.fetch(new Request("https://portfolio.example/api/nope"));
    expect(response.status).toBe(404);
    await expect(response.json()).resolves.toEqual({
      ok: false,
      error: "not_found",
    });
  });
});
