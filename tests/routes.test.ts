import { describe, expect, it } from "vitest";
import { essentialRoutePaths, primaryNavigation } from "../src/app/route-config";

describe("conventional portfolio routes", () => {
  it("keeps every essential escape route available", () => {
    expect(essentialRoutePaths).toEqual([
      "/",
      "/play",
      "/projects",
      "/resume",
      "/ask",
      "/contact",
    ]);
  });

  it("keeps direct professional routes in primary navigation", () => {
    expect(primaryNavigation.map((route) => route.path)).toEqual([
      "/play",
      "/projects",
      "/resume",
      "/ask",
      "/contact",
    ]);
  });
});
