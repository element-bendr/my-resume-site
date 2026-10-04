/// <reference types="vite/client" />

import { describe, expect, it } from "vitest";
import { BLENDER_ART_ASSETS, BLENDER_ART_PLACEMENTS } from "../src/world/art/blender-art-config";
import commandCenterSource from "../src/world/CommandCenter.tsx?raw";
import commandCenterArtSource from "../src/world/art/CommandCenterArt.tsx?raw";

describe("Command Center authored scenery boundary", () => {
  it("uses the registry-backed GLB with bounded decorative loading", () => {
    expect(BLENDER_ART_ASSETS["command-center"]).toBe("/world/art/command-center.glb");
    expect(BLENDER_ART_PLACEMENTS["command-center"]).toEqual([0, 0, 0]);
  });

  it("keeps registry-backed asset and placement use at the art boundary", () => {
    expect(commandCenterArtSource).toContain(
      'import {\n  BLENDER_ART_ASSETS,\n  BLENDER_ART_PLACEMENTS,\n} from "./blender-art-config";',
    );
    expect(commandCenterArtSource).toContain(
      'export const COMMAND_CENTER_ART_ASSET = BLENDER_ART_ASSETS["command-center"];',
    );
    expect(commandCenterArtSource).toContain(
      'export const COMMAND_CENTER_ART_PLACEMENT = BLENDER_ART_PLACEMENTS["command-center"];',
    );
    expect(commandCenterArtSource).toContain(
      "useGLTF(COMMAND_CENTER_ART_ASSET)",
    );
    expect(commandCenterArtSource).toContain(
      "<group position={COMMAND_CENTER_ART_PLACEMENT}>",
    );
    expect(commandCenterArtSource).not.toContain(
      'useGLTF("/world/art/command-center.glb")',
    );
    expect(commandCenterArtSource).not.toContain(
      '<group position={[0, 0, 0]}>',
    );
  });

  it("contains authored-art loading and error fallbacks locally", () => {
    expect(commandCenterArtSource).toContain(
      "class CommandCenterArtBoundary extends Component",
    );
    expect(commandCenterArtSource).toContain("static getDerivedStateFromError");
    expect(commandCenterArtSource).toContain(
      "this.state.failed ? <CommandCenterArtFallback /> : this.props.children",
    );
    expect(commandCenterArtSource).toContain(
      "<Suspense fallback={<CommandCenterArtFallback />}>",
    );
  });

  it("keeps React-owned interaction and movement feedback in CommandCenter", () => {
    expect(commandCenterSource).toContain(
      'const commandStations = stationsForZone("command-center");',
    );
    expect(commandCenterSource).toContain("<CommandCenterArt />");
    expect(commandCenterSource).toContain("<InteractionStation");
    expect(commandCenterSource).toContain("<MoveTargetMarker movementTarget={movementTarget} />");
  });

  it("does not grant gameplay authority to the authored scene", () => {
    expect(BLENDER_ART_ASSETS["command-center"]).not.toContain("topology");
  });
});
