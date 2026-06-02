import { useState, useEffect } from "react";
import CustomCursor from "./components/CustomCursor";
import Header from "./components/Header";

import PerformanceMonitor from "./components/PerformanceMonitor";
import TerminalLogs from "./components/TerminalLogs";
import SettingsPanel from "./components/SettingsPanel";
import AudioVisualizer from "./components/AudioVisualizer";
import SystemControlDock from "./components/SystemControlDock";

export default function App() {
  // Global App States
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isDiagnosticsRunning, setIsDiagnosticsRunning] = useState(false);
  const [isMonitorOpen, setIsMonitorOpen] = useState(false);
  const [isCaptureFlash, setIsCaptureFlash] = useState(false);
  const [isCaptureModalOpen, setIsCaptureModalOpen] = useState(false);
  const [capturedTime, setCapturedTime] = useState("");
  const [newLogs, setNewLogs] = useState([]);

  const addTerminalLog = (logText) => {
    const timestamp = new Date().toLocaleTimeString();
    setNewLogs((prev) => [...prev, `[${timestamp}] ${logText}`]);
  };

  // Settings Object
  const [settings, setSettings] = useState({
    customCursor: false,
    scanlines: false,
    ambientGrid: false,
    performanceMonitor: false,
    terminalLogs: false,
    hue: 0,
  });

  // Handle setting updates
  const handleToggleSetting = (key) => {
    setSettings((prev) => {
      const updated = { ...prev, [key]: !prev[key] };
      // Sync monitor setting state with local panel state
      if (key === "performanceMonitor") {
        setIsMonitorOpen(updated.performanceMonitor);
      }
      return updated;
    });
  };

  const handleHueChange = (newHue) => {
    setSettings((prev) => ({ ...prev, hue: newHue }));
  };

  // Run screen capture flash effect
  const triggerScreenCapture = () => {
    setIsCaptureFlash(true);
    const now = new Date();
    setCapturedTime(now.toLocaleTimeString() + " " + now.toLocaleDateString());
    setTimeout(() => {
      setIsCaptureFlash(false);
      setIsCaptureModalOpen(true);
    }, 150);
  };

  return (
    <div 
      className="relative w-screen h-screen overflow-hidden select-none bg-transparent text-[#dbfcff]"
      style={{ 
        // Real-time hue rotation filter to dynamically shift accent colors
        filter: `hue-rotate(${settings.hue}deg)` 
      }}
    >
      {/* Ambient Grid Overlay */}
      {settings.ambientGrid && (
        <div 
          className="fixed inset-0 pointer-events-none opacity-5 z-1" 
          style={{ 
            backgroundImage: "radial-gradient(rgba(0,219,233,0.35) 1px, transparent 1px)", 
            backgroundSize: "32px 32px" 
          }} 
        />
      )}

      {/* Retro CRT Scanlines */}
      {settings.scanlines && <div className="scanlines z-[99]" />}

      {/* Screen Capture Camera Flash Overlay */}
      {isCaptureFlash && (
        <div className="fixed inset-0 bg-white z-[999] pointer-events-none animate-pulse-fast" />
      )}

      {/* HUD Outer Perimeter Border */}
      <div className="hud-perimeter">
      </div>

      {/* Layout Content Frame */}
      <main className="relative w-full h-full z-20 pointer-events-none">
        
        {/* Floating Top Header bar */}
        <Header />

        {/* Expandable Left Side Drawer */}
        <nav className="hidden fixed left-0 top-1/2 -translate-y-1/2 h-2/3 w-1.5 bg-transparent border-l-2 border-primary-fixed-dim/40 shadow-[0_0_15px_rgba(0,219,233,0.15)] md:flex flex-col items-center justify-between py-12 pointer-events-auto group hover:w-60 hover:bg-[#0e0e0ed0] hover:backdrop-blur-md hover:border-primary-container/20 hover:border-r hover:rounded-r-xl transition-all duration-300 ease-in-out overflow-hidden z-30">
          <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 w-full px-5 flex flex-col gap-6 font-mono text-[9px] text-primary/70">
            
            <div className="flex flex-col gap-1 border-b border-primary-container/20 pb-3">
              <span className="font-space text-sm font-bold tracking-tight text-primary-fixed-dim">
                A.I. INTERFACE
              </span>
              <span className="text-[9px] text-primary-container font-semibold tracking-widest uppercase">
                STATUS: OPTIMAL
              </span>
            </div>

            {/* Neural Net Info Block */}
            <div className="flex flex-col gap-2">
              <span className="text-[10px] text-primary font-bold uppercase tracking-wider">Neural Synapses</span>
              <div className="flex justify-between">
                <span>ACTIVE_REGISTERS:</span>
                <span className="text-primary-container">12,804 / 16,384</span>
              </div>
              <div className="flex justify-between">
                <span>SYNAPSE_LOAD:</span>
                <span className="text-primary-container">34.2 GFLOP/s</span>
              </div>
              <div className="flex justify-between">
                <span>LATENCY_SIGMA:</span>
                <span className="text-primary-container">0.02ms</span>
              </div>
            </div>

            {/* Hardware Metrics Block */}
            <div className="flex flex-col gap-2 border-t border-primary-container/10 pt-3">
              <span className="text-[10px] text-primary font-bold uppercase tracking-wider">A.I. CORES</span>
              <div className="flex justify-between">
                <span>CORE_TEMP_AVG:</span>
                <span className="text-primary-container">44.6°C</span>
              </div>
              <div className="flex justify-between">
                <span>COOLING_FANS:</span>
                <span className="text-primary-container">ACTIVE (45%)</span>
              </div>
              <div className="flex justify-between">
                <span>VOLTAGE_BUS:</span>
                <span className="text-primary-container">1.246 V</span>
              </div>
            </div>

            <div className="text-[8px] text-primary/30 uppercase tracking-widest mt-4">
              JARVIS_SYSTEM_KERNEL_V4.2.22
            </div>
          </div>
        </nav>



        {/* Left corner console log terminal */}
        {settings.terminalLogs && (
          <TerminalLogs 
            isDiagnosticsRunning={isDiagnosticsRunning} 
            onDiagnosticsComplete={() => setIsDiagnosticsRunning(false)}
            newLogs={newLogs}
          />
        )}

        {/* Right corner performance resource metrics panels */}
        <PerformanceMonitor isEnabled={isMonitorOpen} />

        {/* Voice Vocal Waveform visualizer */}
        <AudioVisualizer isActive={isListening} />

        {/* Settings control panel */}
        <SettingsPanel 
          isOpen={isSettingsOpen} 
          settings={settings}
          onToggleSetting={handleToggleSetting}
          onHueChange={handleHueChange}
        />

        {/* Bottom float control dock */}
        <SystemControlDock 
          isSettingsOpen={isSettingsOpen}
          onToggleSettings={() => setIsSettingsOpen(!isSettingsOpen)}
          isListening={isListening}
          onToggleListening={async () => {
            if (isListening) {
              setIsListening(false);
            } else {
              setIsListening(true);
              setIsProcessing(false);
              addTerminalLog("Initializing mic stream...");
              try {
                // 1. Listen for voice command
                const listenRes = await fetch("http://127.0.0.1:8000/api/voice/listen", { method: "POST" });
                const listenData = await listenRes.json();
                
                if (listenData.success && listenData.data.text) {
                  const queryText = listenData.data.text;
                  addTerminalLog(`USER: "${queryText}"`);
                  setIsListening(false);
                  setIsProcessing(true);
                  
                  // 2. Execute command
                  addTerminalLog(`ROUTING: "${queryText}"`);
                  const commandRes = await fetch("http://127.0.0.1:8000/api/command", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ command: queryText })
                  });
                  const commandData = await commandRes.json();
                  setIsProcessing(false);
                  
                  if (commandData.success) {
                    addTerminalLog(`JARVIS: ${commandData.message}`);
                    if (commandData.data.filepath) {
                      addTerminalLog(`PATH: ${commandData.data.filepath}`);
                    }
                  } else {
                    addTerminalLog(`ERROR: ${commandData.message}`);
                  }
                } else {
                  addTerminalLog("AI_ENGINE: No speech recognized.");
                  setIsListening(false);
                }
              } catch (err) {
                addTerminalLog("NETWORK_ERROR: Connection to backend (port 8000) failed.");
                console.error("Connection error:", err);
                setIsListening(false);
              }
            }
          }}
          isDiagnosticsRunning={isDiagnosticsRunning}
          onStartDiagnostics={() => setIsDiagnosticsRunning(true)}
          isMonitorOpen={isMonitorOpen}
          onToggleMonitor={() => {
            setIsMonitorOpen(!isMonitorOpen);
            setSettings((prev) => ({ ...prev, performanceMonitor: !isMonitorOpen }));
          }}
          onTriggerCapture={triggerScreenCapture}
        />

      </main>

      {/* Mockup Screen Capture View Modal */}
      {isCaptureModalOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-[100] pointer-events-auto p-4 select-none">
          <div className="glass-panel w-full max-w-[520px] rounded-2xl p-6 relative flex flex-col gap-4 border border-primary-container/40 animate-scale-in">
            {/* Modal Title */}
            <div className="flex justify-between items-center border-b border-primary-container/20 pb-3">
              <div className="flex items-center gap-2 font-mono text-[11px] font-bold text-primary-container tracking-wider">
                <span className="material-symbols-outlined text-sm">photo_camera</span>
                <span>HUD_SNAPSHOT_PREVIEW</span>
              </div>
              <button 
                onClick={() => setIsCaptureModalOpen(false)}
                className="text-primary/50 hover:text-primary-container font-mono text-[10px] cursor-pointer"
              >
                CLOSE
              </button>
            </div>
            
            {/* Mock Screen Rendering */}
            <div className="relative border border-primary-container/20 rounded-lg overflow-hidden aspect-[16/10] bg-[#1a1a1a] flex items-center justify-center group">
              {/* Radial overlay */}
              <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(0,219,233,0.06),transparent_80%)]" />
              
              {/* Mock captured reticle drawing */}
              <div className="w-16 h-16 rounded-full border border-primary-container/30 border-dashed animate-spin flex items-center justify-center opacity-65">
                <div className="w-1 h-1 bg-primary-container rounded-full" />
              </div>
              
              {/* Overlay labels */}
              <div className="absolute top-3 left-4 font-mono text-[6px] text-primary/40 flex flex-col">
                <span>SNAPSHOT_V4</span>
                <span>TIME: {capturedTime}</span>
              </div>
              
              <div className="absolute bottom-3 right-4 font-mono text-[6px] text-primary-container/50">
                JARVIS_OS_SECURE_EXCEL_EXPORT
              </div>
            </div>

            {/* Info Message & Action */}
            <div className="flex flex-col gap-3">
              <p className="text-[10px] font-mono text-primary/70 leading-relaxed">
                System snapshot successfully saved to local vault cache folder. Metadata parameters have been injected.
              </p>
              <button
                onClick={() => setIsCaptureModalOpen(false)}
                className="w-full py-2 bg-primary-container/25 text-primary-container font-space text-[11px] font-bold border border-primary-container/35 rounded-lg hover:bg-primary-container/40 hover:border-primary-container/60 transition-all cursor-pointer box-glow-cyan active:scale-95 text-center"
              >
                CONFIRM SNAPSHOT EXPORT
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Custom responsive mouse reticle pointer */}
      <CustomCursor isEnabled={settings.customCursor} />
    </div>
  );
}
