import { InteractionStation } from "../InteractionStation";
import { stationsForZone } from "../world-config";
import type { ZoneId } from "../world-topology";
import type { DistrictProps } from "./types";

interface DistrictStationsProps extends DistrictProps {
  zoneId: ZoneId;
}

export function DistrictStations({
  zoneId,
  nearbyStationId,
  onSelectStation,
}: DistrictStationsProps) {
  return (
    <>
      {stationsForZone(zoneId).map((station) => (
        <InteractionStation
          key={station.id}
          station={station}
          nearby={nearbyStationId === station.id}
          onSelect={() => onSelectStation(station)}
        />
      ))}
    </>
  );
}
