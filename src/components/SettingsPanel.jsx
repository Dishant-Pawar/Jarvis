import { useState } from "react";

export default function SettingsPanel({ 
  isOpen, 
  settings, 
  onToggleSetting, 
  onHueChange 
}) {
  if (!isOpen) return null;

  return (
    <div className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[320px] glass-panel rounded-xl p-6 z-50 pointer-events-auto select-none flex flex-col gap-5 border border-primary-container/30">
      
      {/* Panel Header */}
      <div className="flex justify-between items-center border-b border-primary-container/20 pb-3 font-mono text-[10px] tracking-wider text-primary-fixed-dim/90 font-bold">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-xs">settings</span>
          <span>HUD_SETTINGS_v4</span>
        </div>
        <span className="text-[8px] text-primary/30 font-normal">CONFIG_ROOT</span>
      </div>

      {/* Toggles */}
      <div className="flex flex-col gap-4">
        
        {/* Custom Cursor Toggle */}
        <div className="flex justify-between items-center">
          <div className="flex flex-col gap-0.5">
            <span className="text-[11px] font-space font-semibold tracking-wide">HUD Custom Cursor</span>
            <span className="text-[8px] text-primary/45 font-mono">REPLACES DEFAULT MOUSE pointer</span>
          </div>
          <button 
            onClick={() => onToggleSetting("customCursor")}
            className={`w-9 h-5 rounded-full p-0.5 transition-colors duration-300 ${
              settings.customCursor ? "bg-primary-container" : "bg-primary/20"
            }`}
          >
            <div className={`w-4 h-4 rounded-full bg-surface transition-transform duration-300 ${
              settings.customCursor ? "translate-x-4" : "translate-x-0"
            }`} />
          </button>
        </div>

        {/* Scanlines Toggle */}
        <div className="flex justify-between items-center">
          <div className="flex flex-col gap-0.5">
            <span className="text-[11px] font-space font-semibold tracking-wide">Scanline Overlay</span>
            <span className="text-[8px] text-primary/45 font-mono">SIMULATES CRT/HOLOGRAM GRID LINES</span>
          </div>
          <button 
            onClick={() => onToggleSetting("scanlines")}
            className={`w-9 h-5 rounded-full p-0.5 transition-colors duration-300 ${
              settings.scanlines ? "bg-primary-container" : "bg-primary/20"
            }`}
          >
            <div className={`w-4 h-4 rounded-full bg-surface transition-transform duration-300 ${
              settings.scanlines ? "translate-x-4" : "translate-x-0"
            }`} />
          </button>
        </div>

        {/* Grid Overlay Toggle */}
        <div className="flex justify-between items-center">
          <div className="flex flex-col gap-0.5">
            <span className="text-[11px] font-space font-semibold tracking-wide">Ambient Grid dots</span>
            <span className="text-[8px] text-primary/45 font-mono">BACKGROUND RADIAL MATRIX</span>
          </div>
          <button 
            onClick={() => onToggleSetting("ambientGrid")}
            className={`w-9 h-5 rounded-full p-0.5 transition-colors duration-300 ${
              settings.ambientGrid ? "bg-primary-container" : "bg-primary/20"
            }`}
          >
            <div className={`w-4 h-4 rounded-full bg-surface transition-transform duration-300 ${
              settings.ambientGrid ? "translate-x-4" : "translate-x-0"
            }`} />
          </button>
        </div>

        {/* High Performance Toggle */}
        <div className="flex justify-between items-center">
          <div className="flex flex-col gap-0.5">
            <span className="text-[11px] font-space font-semibold tracking-wide">Performance Monitor</span>
            <span className="text-[8px] text-primary/45 font-mono">LIVESTREAM STATS IN TOP RIGHT</span>
          </div>
          <button 
            onClick={() => onToggleSetting("performanceMonitor")}
            className={`w-9 h-5 rounded-full p-0.5 transition-colors duration-300 ${
              settings.performanceMonitor ? "bg-primary-container" : "bg-primary/20"
            }`}
          >
            <div className={`w-4 h-4 rounded-full bg-surface transition-transform duration-300 ${
              settings.performanceMonitor ? "translate-x-4" : "translate-x-0"
            }`} />
          </button>
        </div>

        {/* Diagnostics Terminal Toggle */}
        <div className="flex justify-between items-center">
          <div className="flex flex-col gap-0.5">
            <span className="text-[11px] font-space font-semibold tracking-wide">Diagnostics Terminal</span>
            <span className="text-[8px] text-primary/45 font-mono">SYS_DIAG_TERMINAL CONSOLE</span>
          </div>
          <button 
            onClick={() => onToggleSetting("terminalLogs")}
            className={`w-9 h-5 rounded-full p-0.5 transition-colors duration-300 ${
              settings.terminalLogs ? "bg-primary-container" : "bg-primary/20"
            }`}
          >
            <div className={`w-4 h-4 rounded-full bg-surface transition-transform duration-300 ${
              settings.terminalLogs ? "translate-x-4" : "translate-x-0"
            }`} />
          </button>
        </div>

        {/* Color Hue shift */}
        <div className="flex flex-col gap-2 mt-2 pt-2 border-t border-primary-container/10">
          <div className="flex justify-between items-center">
            <span className="text-[11px] font-space font-semibold tracking-wide">HUD Hue Shift</span>
            <span className="text-[9px] font-mono text-primary-container font-semibold">{settings.hue}°</span>
          </div>
          <input 
            type="range" 
            min="0" 
            max="360" 
            value={settings.hue}
            onChange={(e) => onHueChange(Number(e.target.value))}
            className="w-full h-1 bg-primary/20 rounded-lg appearance-none cursor-pointer accent-primary-container"
          />
          <span className="text-[7px] text-primary/30 font-mono self-end uppercase">DYNAMIC_FILTER_ROTATION</span>
        </div>

      </div>

    </div>
  );
}
