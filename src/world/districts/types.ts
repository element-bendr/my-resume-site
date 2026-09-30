import type { StationConfig, StationId } from "../world-config";

export interface DistrictProps {
  nearbyStationId: StationId | null;
  onSelectStation: (station: StationConfig) => void;
}
