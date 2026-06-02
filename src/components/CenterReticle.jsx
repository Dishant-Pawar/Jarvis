import { useState, useEffect } from "react";

export default function CenterReticle({ isListening, isProcessing, isDiagnosticsRunning }) {
  const [coords, setCoords] = useState({ x: 0, y: 0 });
  const [heading, setHeading] = useState(0);

  useEffect(() => {
    const handleMouseMove = (e) => {
      // Calculate coordinates relative to screen center
      const centerX = window.innerWidth / 2;
      const centerY = window.innerHeight / 2;
      const x = Math.round(e.clientX - centerX);
      const y = Math.round(centerY - e.clientY); // Cartesian coords
      setCoords({ x, y });

      // Calculate angle from center to mouse position
      const rad = Math.atan2(y, x);
      let deg = Math.round(rad * (180 / Math.PI));
      if (deg < 0) deg = 360 + deg;
      setHeading(deg);
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  // Determine reticle colors based on system state
  let statusColor = "rgba(0, 219, 233, 0.4)"; // Default cyan
  let statusRingGlow = "shadow-[0_0_15px_rgba(0,219,233,0.15)]";
  let pulseClass = "";

  if (isListening) {
    statusColor = "rgba(255, 180, 171, 0.6)"; // Error / warning red-orange tint
    statusRingGlow = "shadow-[0_0_20px_rgba(255,180,171,0.4)]";
    pulseClass = "animate-ping";
  } else if (isProcessing) {
    statusColor = "rgba(173, 198, 255, 0.6)"; // Blue tint
    statusRingGlow = "shadow-[0_0_20px_rgba(173,198,255,0.4)] font-bold animate-pulse";
  } else if (isDiagnosticsRunning) {
    statusColor = "rgba(0, 240, 255, 0.8)";
    statusRingGlow = "shadow-[0_0_25px_rgba(0,240,255,0.5)]";
  }

  return (
    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none z-10 select-none flex flex-col items-center justify-center">
      {/* Outer Rotating Ring */}
      <div className={`relative w-[280px] h-[280px] rounded-full border border-dashed flex items-center justify-center transition-colors duration-500 ${statusRingGlow}`}
           style={{ borderColor: statusColor }}>
        
        {/* Animated Spin Ring */}
        <div className="absolute inset-2 rounded-full border border-primary-fixed-dim/10 animate-spin-slow border-t-primary-container/40 border-b-primary-container/40" />

        {/* Opposite Rotating Ring */}
        <div className="absolute inset-8 rounded-full border border-dashed border-primary-fixed/20 animate-spin-reverse" />
        
        {/* Reticle Target Crosshairs */}
        <div className="absolute top-0 bottom-0 w-[1px] bg-primary-fixed-dim/10" />
        <div className="absolute left-0 right-0 h-[1px] bg-primary-fixed-dim/10" />
        
        {/* Dynamic coordinate readout */}
        <div className="absolute top-[-35px] text-center font-mono text-[9px] text-primary-fixed-dim/60 tracking-wider">
          <div className="flex gap-2">
            <span>AZM: <span className="text-primary-container font-semibold">{heading}°</span></span>
            <span>RNG: <span className="text-primary-container font-semibold">{Math.round(Math.sqrt(coords.x ** 2 + coords.y ** 2))}</span></span>
          </div>
        </div>

        {/* Left Coordinates details */}
        <div className="absolute left-[-55px] text-left font-mono text-[8px] text-primary-fixed-dim/40 flex flex-col">
          <span>X: {coords.x}</span>
          <span>Y: {coords.y}</span>
        </div>

        {/* Right HUD brackets */}
        <div className="absolute right-[-45px] font-mono text-[8px] text-primary-container/50 flex flex-col items-end">
          <span>LOCK_ON</span>
          <span className="text-[7px] text-primary/30">HUD_RETICLE_V4</span>
        </div>

        {/* Center Target Dot */}
        <div className={`relative w-2 h-2 rounded-full transition-colors duration-500 ${pulseClass}`}
             style={{ backgroundColor: statusColor }} />
      </div>


    </div>
  );
}
