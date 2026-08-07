import React, { useRef, useEffect } from 'react';
import { Panel } from '../common/Panel';
import { usePolling } from '../../hooks/usePolling';
import { api } from '../../lib/api';

export const RadarMapPanel: React.FC = () => {

  const { data: telemetry } = usePolling(api.getTelemetryLatest, 500, true);

  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {

    const canvas = canvasRef.current;

    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    if (!ctx) return;

    let angle = 0;

    let animationId: number;

    const draw = () => {

      const width = canvas.width;
      const height = canvas.height;

      const cx = width / 2;
      const cy = height / 2;

      ctx.clearRect(0, 0, width, height);

      //---------------- GRID ----------------

      ctx.strokeStyle = "#2a3441";
      ctx.lineWidth = 1;

      for (let x = 0; x < width; x += 20) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }

      for (let y = 0; y < height; y += 20) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      //---------------- RINGS ----------------

      ctx.strokeStyle = "#00f0ff";

      [60,120,180].forEach(r=>{
        ctx.beginPath();
        ctx.arc(cx,cy,r,0,Math.PI*2);
        ctx.stroke();
      });

      //---------------- CROSS ----------------

      ctx.beginPath();

      ctx.moveTo(cx,0);
      ctx.lineTo(cx,height);

      ctx.moveTo(0,cy);
      ctx.lineTo(width,cy);

      ctx.stroke();

      //---------------- SWEEP ----------------

      angle += 0.03;

      ctx.save();

      ctx.translate(cx,cy);

      ctx.rotate(angle);

      ctx.strokeStyle="rgba(0,240,255,.5)";

      ctx.beginPath();

      ctx.moveTo(0,0);

      ctx.lineTo(180,0);

      ctx.stroke();

      ctx.restore();

      //---------------- DRONE ----------------

      if(

        telemetry &&

        typeof telemetry.latitude==="number" &&

        typeof telemetry.longitude==="number" &&

        typeof telemetry.altitude==="number" &&

        typeof telemetry.yaw==="number"

      ){

        const dx=Math.sin(telemetry.yaw*Math.PI/180)*80;

        const dy=-Math.cos(telemetry.yaw*Math.PI/180)*80;

        ctx.fillStyle="#00ff41";

        ctx.beginPath();

        ctx.arc(cx+dx,cy+dy,4,0,Math.PI*2);

        ctx.fill();

        ctx.beginPath();

        ctx.moveTo(cx+dx,cy+dy);

        ctx.lineTo(

          cx+dx+Math.sin(telemetry.yaw*Math.PI/180)*15,

          cy+dy-Math.cos(telemetry.yaw*Math.PI/180)*15

        );

        ctx.strokeStyle="#00ff41";

        ctx.stroke();

        ctx.fillStyle="#00ff41";

        ctx.font="10px monospace";

        ctx.fillText(

          `ALT ${telemetry.altitude.toFixed(1)}m`,

          cx+dx+8,

          cy+dy

        );

      }

      animationId=requestAnimationFrame(draw);

    };

    draw();

    return ()=>cancelAnimationFrame(animationId);

  },[telemetry]);

  return(

    <Panel
      title="Interactive Tactical Map"
      className="h-full relative overflow-hidden bg-[#05080c]"
    >

      <canvas

        ref={canvasRef}

        width={800}

        height={600}

        className="absolute inset-0 w-full h-full"

      />

      <div className="absolute bottom-2 left-2 bg-black/70 border border-tactical-border p-2 text-[10px] font-mono text-signal-cyan">

        <div>

          LAT :

          {

            typeof telemetry?.latitude==="number"

            ? telemetry.latitude.toFixed(6)

            : "--"

          }

        </div>

        <div>

          LON :

          {

            typeof telemetry?.longitude==="number"

            ? telemetry.longitude.toFixed(6)

            : "--"

          }

        </div>

        <div>

          ALT :

          {

            typeof telemetry?.altitude==="number"

            ? telemetry.altitude.toFixed(1)

            : "--"

          } m

        </div>

      </div>

    </Panel>

  );

};