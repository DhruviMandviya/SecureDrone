import React, { useRef, useEffect } from 'react';
import { Panel } from '../common/Panel';
import { usePolling } from '../../hooks/usePolling';
import { api } from '../../lib/api';

export const RadarMapPanel: React.FC = () => {
  const { data: telemetry } = usePolling(api.getTelemetryLatest, 200, true);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  // Tactical radar grid render
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let localAngle = 0;
    
    const draw = () => {
       const width = canvas.width;
       const height = canvas.height;
       const cx = width / 2;
       const cy = height / 2;

       ctx.clearRect(0, 0, width, height);

       // Draw grid
       ctx.strokeStyle = '#2a3441';
       ctx.lineWidth = 1;
       const step = 20;
       ctx.beginPath();
       for(let x=0; x<width; x+=step) { ctx.moveTo(x, 0); ctx.lineTo(x, height); }
       for(let y=0; y<height; y+=step) { ctx.moveTo(0, y); ctx.lineTo(width, y); }
       ctx.stroke();

       // Draw crosshairs
       ctx.strokeStyle = '#00f0ff';
       ctx.lineWidth = 0.5;
       ctx.beginPath();
       ctx.moveTo(cx, 0); ctx.lineTo(cx, height);
       ctx.moveTo(0, cy); ctx.lineTo(width, cy);
       ctx.stroke();

       // Draw range rings
       ctx.beginPath();
       ctx.arc(cx, cy, 60, 0, Math.PI * 2);
       ctx.arc(cx, cy, 120, 0, Math.PI * 2);
       ctx.arc(cx, cy, 180, 0, Math.PI * 2);
       ctx.stroke();

       // Draw Sweep
       localAngle = (localAngle + 0.05) % (Math.PI * 2);
       ctx.save();
       ctx.translate(cx, cy);
       ctx.rotate(localAngle);
       
       const gradient = ctx.createConicGradient(0, 0, 0);
       gradient.addColorStop(0, 'rgba(0, 240, 255, 0)');
       gradient.addColorStop(0.2, 'rgba(0, 240, 255, 0.4)');
       gradient.addColorStop(1, 'rgba(0, 240, 255, 0)');
       
       ctx.fillStyle = gradient;
       ctx.beginPath();
       ctx.moveTo(0,0);
       ctx.arc(0, 0, width, 0, Math.PI/4);
       ctx.lineTo(0,0);
       ctx.fill();
       ctx.restore();

       // Draw Drone blip
       if (telemetry) {
          // Fake projection relative to center
          const dx = Math.sin(telemetry.yaw * Math.PI / 180) * 80;
          const dy = -Math.cos(telemetry.yaw * Math.PI / 180) * 80;
          
          ctx.fillStyle = '#00ff41';
          ctx.beginPath();
          ctx.arc(cx + dx, cy + dy, 3, 0, Math.PI * 2);
          ctx.fill();
          
          ctx.strokeStyle = '#00ff41';
          ctx.beginPath();
          ctx.moveTo(cx + dx, cy + dy);
          ctx.lineTo(cx + dx + Math.sin(telemetry.yaw * Math.PI / 180)*15, 
                     cy + dy - Math.cos(telemetry.yaw * Math.PI / 180)*15);
          ctx.stroke();

          ctx.fillStyle = '#00ff41';
          ctx.font = '10px monospace';
          ctx.fillText(`ALT:${telemetry.altitude.toFixed(0)}`, cx + dx + 6, cy + dy + 4);
       }

       requestAnimationFrame(draw);
    };
    
    let animId = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(animId);
  }, [telemetry]);

  return (
    <Panel title="Interactive Tactical Map" className="h-full relative overflow-hidden bg-[#05080c]">
       <canvas 
          ref={canvasRef} 
          width={800} 
          height={600} 
          className="absolute inset-0 w-full h-full object-cover"
       />
       <div className="absolute bottom-2 left-2 flex gap-4 bg-tactical-bg/80 p-2 border border-tactical-border/50 text-[10px] font-mono">
          <div className="flex flex-col text-signal-cyan">
             <span>
  LAT // {telemetry ? telemetry.latitude.toFixed(6) : "--"}
</span>

<span>
  LON // {telemetry ? telemetry.longitude.toFixed(6) : "--"}
</span>
          </div>
       </div>
    </Panel>
  );
};
