import React, { useMemo } from 'react';
import { Panel } from '../common/Panel';
import { usePolling } from '../../hooks/usePolling';
import { api } from '../../lib/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip } from 'recharts';

export const LiveChartsPanel: React.FC = () => {
  const { data: history } = usePolling(api.getTelemetryHistory, 1000);

  const formattedData = useMemo(() => {
    if (!history) return [];

    return history.map((t, index) => ({
        time: index.toString(),
        altitude: t.altitude,
        velocity: t.velocity
    }));
}, [history]);

  return (
    <Panel title="Telemetry Trending Viewer" className="h-[250px] lg:h-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={formattedData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a3441" vertical={false} />
          <XAxis 
             dataKey="time" 
             stroke="#2a3441" 
             tick={{ fill: '#a8b0ba', fontSize: 10, fontFamily: 'monospace' }} 
             tickLine={false} 
             axisLine={{ stroke: '#2a3441' }}
          />
          <YAxis 
             yAxisId="left" 
             stroke="#2a3441" 
             tick={{ fill: '#00f0ff', fontSize: 10, fontFamily: 'monospace' }} 
             axisLine={false}
             tickFormatter={(val: number) => `${val.toFixed(0)}m`}
             domain={['dataMin - 10', 'dataMax + 10']}
          />
           <YAxis 
             yAxisId="right" 
             orientation="right"
             stroke="#2a3441" 
             tick={{ fill: '#00ff41', fontSize: 10, fontFamily: 'monospace' }} 
             axisLine={false}
             tickFormatter={(val:number)=>`${val.toFixed(2)} m/s`}
             domain={['dataMin - 5', 'dataMax + 5']}
          />
          <Tooltip 
             contentStyle={{ backgroundColor: '#0d1117', border: '1px solid #2a3441', color: '#fff', fontSize: '12px' }}
             itemStyle={{ fontFamily: 'monospace', fontWeight: 'bold' }}
             labelStyle={{ fontFamily: 'monospace', color: '#a8b0ba', marginBottom: '4px' }}
          />
          <Line 
             yAxisId="left" 
             type="monotone" 
             dataKey="altitude" 
             stroke="#00f0ff" 
             strokeWidth={2} 
             dot={false}
             isAnimationActive={false}
          />
          <Line
              yAxisId="right"
              type="monotone"
              dataKey="velocity"
              stroke="#00ff41"
              strokeWidth={2}
              dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </Panel>
  );
};
