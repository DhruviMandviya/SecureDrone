import React from "react";
import { Panel } from "../common/Panel";
import { usePolling } from "../../hooks/usePolling";
import { api } from "../../lib/api";

const steps = [
  "AUTHENTICATED",
  "HANDSHAKE",
  "ARMING",
  "ARMED",
  "TAKEOFF",
  "HOVERING",
  "LANDING",
  "COMPLETED"
];

export const MissionProgressPanel: React.FC = () => {

  const { data } = usePolling(
    api.getMission,
    200
  );

  const current = data?.status ?? "";

  const currentIndex = steps.indexOf(current);

  const progress =
  currentIndex >= 0
    ? ((currentIndex + 1) / steps.length) * 100
    : 0;

return (
  <Panel title="MISSION PROGRESS" className="h-full">

    <div className="mb-4">

      <div className="flex justify-between text-[10px] font-mono text-gray-400 mb-1">
        <span>{current || "WAITING..."}</span>
        <span>{progress.toFixed(0)}%</span>
      </div>

      <div className="w-full h-2 bg-gray-800 rounded">
        <div
          className="h-2 bg-cyan-400 rounded transition-all duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>

    </div>

    <div className="space-y-2">

      {steps.map((step, index) => {

        const completed = index < currentIndex;
        const active = index === currentIndex;

        return (

          <div
            key={step}
            className="flex items-center gap-3"
          >

            <div
              className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px]
              ${
                completed
                  ? "bg-green-500 text-black"
                  : active
                  ? "bg-cyan-400 animate-pulse text-black"
                  : "bg-gray-700"
              }`}
            >
              {completed ? "✓" : active ? "▶" : ""}
            </div>

            <span
              className={`font-mono text-sm
              ${
                completed
                  ? "text-green-400"
                  : active
                  ? "text-cyan-300 font-bold"
                  : "text-gray-500"
              }`}
            >
              {step}
            </span>

          </div>

        );

      })}

    </div>

  </Panel>
);
};