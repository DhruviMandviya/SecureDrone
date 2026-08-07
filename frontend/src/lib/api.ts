// Base URL for the SecureDrone Backend
const API_BASE_URL = 'http://127.0.0.1:8000';
const USE_MOCK_FALLBACK = false; // Flips to true if fetch fails to allow UI dev

// ==== TYPES ====
export interface SystemHealth {
  status: 'ok' | 'warning' | 'critical';
  uptime: number;
  components: Record<string, string>;
}

export interface Telemetry {
    timestamp: string;

    latitude: number;
    longitude: number;
    altitude: number;

    velocity: number;

    battery: number;

    pitch: number;
    roll: number;
    yaw: number;

    gps_sats: number;

    mode: string;

    armed: boolean;
}

export interface Session {
  session_id: string;
  established_at: string;
  kem_algorithm: string;
  cipher: string;
  bytes_sent: number;
  bytes_received: number;
  packets_dropped: number;
  active: boolean;
}
export interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
}

export interface SystemStatus {
  ground_station: string;
  active_sessions: number;
  telemetry_packets: number;
  latest_available: boolean;
}

// ==== MOCKS ====
// Self-updating mock telemetry
let mockAltitude = 120.5;
let mockHeading = 45;
let mockBattery = 88;
const generateMockTelemetry = (): Telemetry => {
  mockAltitude += (Math.random() - 0.5) * 2;
  mockHeading = (mockHeading + (Math.random() - 0.4) * 2) % 360;
  mockBattery = Math.max(0, mockBattery - 0.01);
  return {
    timestamp: new Date().toISOString(),
    latitude: 37.7749 + (Math.random() * 0.001 - 0.0005),
    longitude: -122.4194 + (Math.random() * 0.001 - 0.0005),
    altitude: mockAltitude,
    velocity: 15.2 + Math.random(),
    yaw: mockHeading,
    battery: mockBattery,
    mode: 'GUIDED',
    armed: true,
    gps_sats: 14 + Math.floor(Math.random() * 3),
  };
};

const mockHistory: Telemetry[] = Array.from({ length: 50 }).map((_, i) => ({
  ...generateMockTelemetry(),
  timestamp: new Date(Date.now() - (50 - i) * 1000).toISOString(),
}));

// ==== FETCHER ====
async function fetchWithFallback<T>(endpoint: string, mockData: T | (() => T)): Promise<T> {
  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return (await res.json()) as T;
  } catch (error) {
    if (USE_MOCK_FALLBACK) {
      console.warn(`[API Mock] Using fallback for ${endpoint}`);
      return typeof mockData === 'function' ? (mockData as Function)() : mockData;
    }
    throw error;
  }
}

// ==== API METHODS ====
export const api = {
  getServiceInfo: () => fetchWithFallback('/', { name: 'SecureDrone API', version: '1.0.0' }),
  
  getHealth: () => fetchWithFallback<SystemHealth>('/health', {
    status: 'ok',
    uptime: 3600 * 24 * 3, // 3 days
    components: { database: 'ok', mqtt: 'ok', gcs: 'ok' },
  }),

  getStatus: () =>
  fetchWithFallback<SystemStatus>('/status', {
    ground_station: "Running",
    active_sessions: 0,
    telemetry_packets: 0,
    latest_available: false,
  }),

  getSessions: () =>
    fetchWithFallback<Session[]>('/sessions', []),

  getTelemetryLatest: () => fetchWithFallback<Telemetry>('/telemetry/latest', generateMockTelemetry),

  getTelemetryHistory: () => fetchWithFallback<Telemetry[]>('/telemetry/history', () => {
    // Append the latest mock value to history mock to simulate rolling
    const latest = generateMockTelemetry();
    mockHistory.push(latest);
    if (mockHistory.length > 50) mockHistory.shift();
    return [...mockHistory];
  }),
  getLogs: () =>
  fetchWithFallback<LogEntry[]>("/logs", []),
};
