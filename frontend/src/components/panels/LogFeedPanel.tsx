import React from "react";
import { Panel } from "../common/Panel";
import { usePolling } from "../../hooks/usePolling";
import { api } from "../../lib/api";

export const LogFeedPanel: React.FC = () => {

  const { data: logs } = usePolling(api.getLogs, 1000);

  const getColor = (level: string) => {
    switch (level) {
      case "SUCCESS":
        return "text-signal-green";

      case "INFO":
        return "text-[#a8b0ba]";

      case "ERROR":
        return "text-alert-red font-bold";

      default:
        return "text-white";
    }
  };

  return (
    <Panel
      title="MISSION / SECURITY LOG"
      className="h-[360px]"
    >
      <div className="h-[290px] overflow-y-auto overflow-x-hidden font-mono text-xs space-y-2 pr-2">

        {logs
          ?.slice(-50)
          .reverse()
          .map((log, index) => (

            <div
              key={index}
              className="border-b border-tactical-border/20 pb-1"
            >
              <span className="text-[#6b7280]">
                {new Date(log.timestamp).toLocaleTimeString("en-IN", {
                  hour: "2-digit",
                  minute: "2-digit",
                  second: "2-digit",
                })}
              </span>

              <br />

              <span className={getColor(log.level)}>
                {log.message}
              </span>
            </div>

          ))}

      </div>
    </Panel>
  );
};