import React from 'react';
import { Panel } from '../common/Panel';
import { DataReadout } from '../common/DataReadout';
import { usePolling } from '../../hooks/usePolling';
import { api } from '../../lib/api';

export const LiveTelemetryHUD: React.FC = () => {
  const { data: telemetry, loading } = usePolling(
    api.getTelemetryLatest,
    1000,
    true
  );

  if (loading && !telemetry) {
    return (
      <Panel title="Live Telemetry">
        <div className="flex items-center justify-center h-full text-signal-cyan">
          ACQUIRING SIGNAL...
        </div>
      </Panel>
    );
  }

  if (!telemetry) {
    return (
      <Panel title="Live Telemetry">
        <div className="flex items-center justify-center h-full text-alert-red">
          NO TELEMETRY
        </div>
      </Panel>
    );
  }

  return (
    <Panel title="Live Telemetry" className="h-full">
      <div className="grid grid-cols-2 gap-4">

        <DataReadout
          label="BATTERY"
          value={telemetry.battery.toFixed(1)}
          unit="%"
          size="md"
          color={telemetry.battery > 20 ? 'text-signal-green' : 'text-alert-red'}
        />

        <DataReadout
          label="ALTITUDE"
          value={telemetry.altitude.toFixed(2)}
          unit="m"
          size="md"
          color="text-white"
        />

        <DataReadout
          label="VELOCITY"
          value={telemetry.velocity.toFixed(2)}
          unit="m/s"
          size="md"
          color="text-white"
        />

        <DataReadout
          label="YAW"
          value={telemetry.yaw.toFixed(1)}
          unit="°"
          size="md"
          color="text-white"
        />

        <div className="col-span-2 border-t border-tactical-border pt-3">
          <div className="text-xs text-tactical-text mb-2">
            COORDINATES
          </div>

          <div className="font-mono text-signal-cyan flex justify-between">
            <span>LAT: {telemetry.latitude.toFixed(6)}</span>
            <span>LON: {telemetry.longitude.toFixed(6)}</span>
          </div>
        </div>

      </div>
    </Panel>
  );
};