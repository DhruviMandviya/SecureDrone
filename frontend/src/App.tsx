
import { MissionHeader } from './components/panels/MissionHeader';
import { LiveTelemetryHUD } from './components/panels/LiveTelemetryHUD';
import { CryptoStatusPanel } from './components/panels/CryptoStatusPanel';
import { AESStatusPanel } from './components/panels/AESStatusPanel';
import { SystemHealthPanel } from './components/panels/SystemHealthPanel';
import { DroneStatusPanel } from './components/panels/DroneStatusPanel';
import { RadarMapPanel } from './components/panels/RadarMapPanel';
import { LiveChartsPanel } from './components/panels/LiveChartsPanel';
import { DataTablesPanel } from './components/panels/DataTablesPanel';
import { LogFeedPanel } from './components/panels/LogFeedPanel';
import { DataStatsPanel } from './components/panels/DataStatsPanel';

function App() {
  return (
    <div className="min-h-screen bg-tactical-bg text-tactical-text flex flex-col font-sans overflow-x-hidden selection:bg-signal-cyan/30">
      <MissionHeader />
      
      {/* Main Grid Layout */}
      <main className="flex-1 p-2 md:p-4 grid grid-cols-1 md:grid-cols-4 lg:grid-cols-12 gap-2 md:gap-4 lg:grid-rows-[auto_1fr_auto]">
        
        {/* LEFT COLUMN: Systems & Crypto */}
        <div className="md:col-span-1 lg:col-span-3 flex flex-col gap-4">
          <SystemHealthPanel />
          <DroneStatusPanel />
          <CryptoStatusPanel />
          <AESStatusPanel />
        </div>

        {/* CENTER COLUMN: Tactical View & Telemetry */}
        <div className="md:col-span-2 lg:col-span-6 flex flex-col gap-4">
          <RadarMapPanel />
          <div className="h-[200px]">
             <LiveTelemetryHUD />
          </div>
          <LiveChartsPanel />
          <DataTablesPanel />
        </div>

        {/* RIGHT COLUMN: Logs & Stats */}
        <div className="md:col-span-1 lg:col-span-3 flex flex-col gap-4">
          <LogFeedPanel />
          <DataStatsPanel />
        </div>

      </main>
      
      <footer className="h-6 border-t border-tactical-border bg-tactical-bg px-4 flex items-center justify-between text-[10px] text-tactical-text/50 font-mono">
        <span>V 1.0.4-SECURE</span>
        <span>NODE: GCS-ALPHA</span>
        <span>LINK: SECURE-KEM-AES</span>
      </footer>
    </div>
  );
}

export default App;
