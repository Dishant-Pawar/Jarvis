import { useState, useEffect } from "react";

export default function PerformanceMonitor({ isEnabled }) {
  const [cpuHistory, setCpuHistory] = useState(Array(15).fill(25));
  const [ramHistory, setRamHistory] = useState(Array(15).fill(48));
  const [gpuHistory, setGpuHistory] = useState(Array(15).fill(15));
  const [netHistory, setNetHistory] = useState(Array(15).fill(10));

  const [currentStats, setCurrentStats] = useState({
    cpu: 25,
    ram: 48,
    gpu: 15,
    net: 1.2,
  });

  useEffect(() => {
    if (!isEnabled) return;

    const interval = setInterval(() => {
      // Generate realistic jittery numbers
      const cpuVal = Math.max(10, Math.min(95, Math.round(currentStats.cpu + (Math.random() - 0.5) * 15)));
      const ramVal = Math.max(40, Math.min(85, Math.round(currentStats.ram + (Math.random() - 0.5) * 4)));
      const gpuVal = Math.max(5, Math.min(90, Math.round(currentStats.gpu + (Math.random() - 0.5) * 8)));
      const netVal = Math.max(0.1, Math.min(25.0, Number((currentStats.net + (Math.random() - 0.5) * 2).toFixed(1))));

      setCurrentStats({
        cpu: cpuVal,
        ram: ramVal,
        gpu: gpuVal,
        net: netVal,
      });

      setCpuHistory((prev) => [...prev.slice(1), cpuVal]);
      setRamHistory((prev) => [...prev.slice(1), ramVal]);
      setGpuHistory((prev) => [...prev.slice(1), gpuVal]);
      setNetHistory((prev) => [...prev.slice(1), Math.round((netVal / 25) * 100)]);
    }, 1000);

    return () => clearInterval(interval);
  }, [isEnabled, currentStats]);

  if (!isEnabled) return null;

  // Helper to generate SVG Path from data values
  const generateSvgPath = (history) => {
    const width = 120;
    const height = 40;
    const step = width / (history.length - 1);
    
    return history
      .map((val, idx) => {
        const x = idx * step;
        const y = height - (val / 100) * height;
        return `${idx === 0 ? "M" : "L"} ${x} ${y}`;
      })
      .join(" ");
  };

  const renderPanel = (title, currentVal, unit, history, color, icon) => {
    const pathData = generateSvgPath(history);
    return (
      <div className="glass-panel rounded-xl p-4 flex flex-col gap-2 relative overflow-hidden group hover:glass-panel-active transition-all duration-300">
        {/* Subtle background glow */}
        <div className="absolute inset-0 bg-primary-container/2 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
        
        {/* Top title and icon */}
        <div className="flex justify-between items-center border-b border-primary-container/10 pb-1.5 font-mono text-[10px] tracking-wider text-primary-fixed-dim/80">
          <div className="flex items-center gap-1.5">
            <span className="material-symbols-outlined text-xs" style={{ color }}>{icon}</span>
            <span>{title}</span>
          </div>
          <span className="text-[9px] text-primary/40 font-normal">SYS_MON_V4</span>
        </div>

        {/* Layout with graph and stats */}
        <div className="flex justify-between items-end gap-4 mt-1">
          {/* Real-time Graph SVG */}
          <div className="flex-1 h-10">
            <svg viewBox="0 0 120 40" className="w-full h-full overflow-visible">
              {/* Grid Lines */}
              <line x1="0" y1="10" x2="120" y2="10" stroke="rgba(0, 219, 233, 0.05)" strokeWidth="0.5" />
              <line x1="0" y1="20" x2="120" y2="20" stroke="rgba(0, 219, 233, 0.05)" strokeWidth="0.5" />
              <line x1="0" y1="30" x2="120" y2="30" stroke="rgba(0, 219, 233, 0.05)" strokeWidth="0.5" />
              
              {/* Animated Path */}
              <path
                d={pathData}
                fill="none"
                stroke={color}
                strokeWidth="1.5"
                className="transition-all duration-1000 ease-in-out"
              />
            </svg>
          </div>

          {/* Current percentage/value display */}
          <div className="flex flex-col items-end justify-end leading-none">
            <span className="font-space text-lg font-bold text-glow-cyan" style={{ color }}>
              {currentVal}
            </span>
            <span className="text-[8px] text-primary-fixed-dim/60 font-mono tracking-widest mt-1 uppercase">
              {unit}
            </span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="fixed right-margin-desktop top-24 w-[280px] flex flex-col gap-4 z-30 select-none pointer-events-auto max-h-[calc(100vh-200px)] overflow-y-auto custom-scrollbar pr-1">
      {renderPanel("CPU CORE LOAD", currentStats.cpu, "% LOAD", cpuHistory, "#00dbe9", "developer_board")}
      {renderPanel("SYSTEM MEMORY", currentStats.ram, "% OF 32GB", ramHistory, "#adc6ff", "memory")}
      {renderPanel("GPU PROCESSOR", currentStats.gpu, "% LOAD", gpuHistory, "#7df4ff", "memory_alt")}
      {renderPanel("NETWORK BANDWIDTH", currentStats.net, "MB/S RATE", netHistory, "#faf3ff", "dynamic_form")}
    </div>
  );
}
