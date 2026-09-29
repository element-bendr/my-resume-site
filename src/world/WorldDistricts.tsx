import { lazy, Suspense } from "react";
import type { StationConfig } from "./world-config";
import type { ZoneId } from "./world-topology";

const BuildLab = lazy(() => import("./districts/BuildLab"));
const AutomationLab = lazy(() => import("./districts/AutomationLab"));
const ClientStreet = lazy(() => import("./districts/ClientStreet"));
const TimelineCorridor = lazy(() => import("./districts/TimelineCorridor"));
const HobbyDistrict = lazy(() => import("./districts/HobbyDistrict"));

interface WorldDistrictsProps {
  loadedZones: ReadonlySet<ZoneId>;
  nearbyStationId: StationConfig["id"] | null;
  onSelectStation: (station: StationConfig) => void;
}

export function WorldDistricts({
  loadedZones,
  nearbyStationId,
  onSelectStation,
}: WorldDistrictsProps) {
  return (
    <Suspense fallback={null}>
      {loadedZones.has("build-lab") ? (
        <BuildLab nearbyStationId={nearbyStationId} onSelectStation={onSelectStation} />
      ) : null}
      {loadedZones.has("automation-lab") ? (
        <AutomationLab nearbyStationId={nearbyStationId} onSelectStation={onSelectStation} />
      ) : null}
      {loadedZones.has("client-street") ? (
        <ClientStreet nearbyStationId={nearbyStationId} onSelectStation={onSelectStation} />
      ) : null}
      {loadedZones.has("timeline") ? (
        <TimelineCorridor nearbyStationId={nearbyStationId} onSelectStation={onSelectStation} />
      ) : null}
      {loadedZones.has("hobby-district") ? (
        <HobbyDistrict nearbyStationId={nearbyStationId} onSelectStation={onSelectStation} />
      ) : null}
    </Suspense>
  );
}
