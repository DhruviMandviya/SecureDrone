import React, { useState } from 'react';
import { Panel } from '../common/Panel';
import { usePolling } from '../../hooks/usePolling';
import { api } from '../../lib/api';

export const DataTablesPanel: React.FC = () => {
  const { data: history } = usePolling(api.getTelemetryHistory, 1000);
  const { data: sessions } = usePolling(api.getSessions, 5000);

  const [tab, setTab] = useState<'telemetry' | 'sessions'>('telemetry');

  return (
    <Panel
      title="Telemetry History & Session Logs"
      className="h-[360px]"
      headerRight={
        <div className="flex gap-1">
          <button
            onClick={() => setTab('telemetry')}
            className={`px-2 py-1 text-xs ${
              tab === 'telemetry'
                ? 'bg-tactical-text text-black font-bold'
                : 'text-tactical-text hover:bg-tactical-border'
            }`}
          >
            TLM LOG
          </button>

          <button
            onClick={() => setTab('sessions')}
            className={`px-2 py-1 text-xs ${
              tab === 'sessions'
                ? 'bg-tactical-text text-black font-bold'
                : 'text-tactical-text hover:bg-tactical-border'
            }`}
          >
            SEC. SESS
          </button>
        </div>
      }
    >
      <div className="h-[290px] overflow-y-auto overflow-x-hidden">

        {tab === 'telemetry' && (
          <table className="w-full font-mono text-xs">
            <thead className="sticky top-0 bg-[#0d1117] border-b border-tactical-border text-white z-10">
              <tr>
                <th className="text-left px-2 py-2">TIME</th>
                <th className="text-left px-2 py-2">LAT / LON</th>
                <th className="text-right px-2 py-2">ALT</th>
                <th className="text-right px-2 py-2">VEL</th>
                <th className="text-center px-2 py-2">BAT</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-tactical-border">
              {history
                ?.slice(-50)
                .reverse()
                .map((row, i) => (
                  <tr
                    key={i}
                    className="hover:bg-signal-cyan/5 transition-colors"
                  >
                    <td className="px-2 py-1 whitespace-nowrap">
                      {new Date(row.timestamp).toLocaleTimeString("en-IN", {
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit",
                      })}
                    </td>

                    <td className="px-2 py-1">
                      {row.latitude.toFixed(4)} / {row.longitude.toFixed(4)}
                    </td>

                    <td className="text-right px-2 py-1">
                      {row.altitude.toFixed(1)} m
                    </td>

                    <td className="text-right px-2 py-1">
                      {row.velocity.toFixed(1)} m/s
                    </td>

                    <td className="text-center px-2 py-1">
                      {row.battery.toFixed(0)}%
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        )}

        {tab === 'sessions' && (
          <table className="w-full font-mono text-xs">
            <thead className="sticky top-0 bg-[#0d1117] border-b border-tactical-border text-white z-10">
              <tr>
                <th className="text-left px-2 py-2">SESSION</th>
                <th className="text-left px-2 py-2">ALGORITHM</th>
                <th className="text-right px-2 py-2">STATUS</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-tactical-border">
              {sessions?.map((row, i) => (
                <tr
                  key={i}
                  className="hover:bg-signal-cyan/5 transition-colors"
                >
                  <td className="px-2 py-1">
                    {row.session_id}
                  </td>

                  <td className="px-2 py-1">
                    {row.kem_algorithm}
                  </td>

                  <td className="text-right px-2 py-1">
                    {row.active ? (
                      <span className="text-green-400 font-bold">
                        ACTIVE
                      </span>
                    ) : (
                      <span className="text-red-400">
                        CLOSED
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

      </div>
    </Panel>
  );
};