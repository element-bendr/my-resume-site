import { describe, expect, it } from "vitest";
import { essentialRoutePaths } from "../src/app/route-config";
import { STATIONS, stationsForZone } from "../src/world/world-config";
import { isWalkablePoint, zoneAtPoint } from "../src/world/world-topology";

describe("Command Center Ask Terminal integration", () => {
  it("keeps the Ask terminal in its legal Command Center interaction area", () => {
    const terminal = STATIONS.find((station) => station.id === "ask-terminal");

    expect(terminal).toBeDefined();
    if (!terminal) return;
    expect(terminal).toMatchObject({ kind: "ask", zoneId: "command-center" });
    expect(stationsForZone("command-center")).toContain(terminal);
    expect(isWalkablePoint(terminal.interactionPoint)).toBe(true);
    expect(zoneAtPoint(terminal.interactionPoint)).toBe("command-center");
  });

  it("keeps /ask as an essential conventional route", () => {
    expect(essentialRoutePaths).toContain("/ask");
  });
});
