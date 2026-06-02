export default function SystemControlDock({
  isSettingsOpen,
  onToggleSettings,
  isListening,
  onToggleListening,
  isDiagnosticsRunning,
  onStartDiagnostics,
  isMonitorOpen,
  onToggleMonitor,
  onTriggerCapture
}) {
  return (
    <nav className="fixed bottom-8 left-1/2 -translate-x-1/2 rounded-full px-6 py-3 bg-surface-container-lowest/15 text-primary border-[0.5px] border-primary-container/30 backdrop-blur-2xl bg-black/40 shadow-[0_0_25px_rgba(0,219,233,0.12)] flex items-center gap-6 z-40 select-none pointer-events-auto">
      
      {/* Settings Button */}
      <button
        onClick={onToggleSettings}
        aria-label="Settings"
        className={`flex items-center justify-center w-11 h-11 rounded-full transition-all duration-300 hover:scale-110 active:scale-95 cursor-pointer ${
          isSettingsOpen 
            ? "text-primary-container bg-primary-container/10 border border-primary-container/35 box-glow-cyan" 
            : "text-on-surface-variant hover:text-primary-fixed-dim"
        }`}
      >
        <span className="material-symbols-outlined text-[22px]">settings</span>
      </button>

      {/* Execute Diagnostics Button */}
      <button
        onClick={onStartDiagnostics}
        disabled={isDiagnosticsRunning}
        aria-label="Execute Diagnostics"
        className={`flex items-center justify-center w-11 h-11 rounded-full transition-all duration-300 hover:scale-110 active:scale-95 cursor-pointer ${
          isDiagnosticsRunning 
            ? "text-primary/30 border border-primary/10 cursor-not-allowed" 
            : "text-on-surface-variant hover:text-primary-fixed-dim hover:bg-primary-container/5"
        }`}
      >
        <span className={`material-symbols-outlined text-[22px] ${isDiagnosticsRunning ? "" : "hover:text-glow-cyan"}`} 
              style={{ fontVariationSettings: "'FILL' 1" }}>
          play_arrow
        </span>
      </button>

      {/* Talk (Active / Center focus Mic) */}
      <button
        onClick={onToggleListening}
        aria-label="Talk with JARVIS"
        className={`relative flex items-center justify-center w-13 h-13 rounded-full transition-all duration-300 hover:scale-110 active:scale-95 cursor-pointer ${
          isListening
            ? "bg-error-container/20 text-error ring-1 ring-error/50 shadow-[0_0_15px_rgba(255,180,171,0.4)]"
            : "bg-primary-container/20 text-primary-container border border-primary-container/30 shadow-[0_0_12px_rgba(0,219,233,0.25)] hover:bg-primary-container/30 hover:border-primary-container/50"
        }`}
      >
        <span className="material-symbols-outlined text-[26px]" style={{ fontVariationSettings: "'FILL' 1" }}>
          {isListening ? "mic_off" : "mic"}
        </span>
        
        {/* Breathing ring when listening */}
        {isListening && (
          <span className="absolute -inset-1 rounded-full border border-error/40 animate-ping opacity-60 pointer-events-none" />
        )}
      </button>

      {/* Monitor Toggle Button */}
      <button
        onClick={onToggleMonitor}
        aria-label="Toggle Resource Monitor"
        className={`flex items-center justify-center w-11 h-11 rounded-full transition-all duration-300 hover:scale-110 active:scale-95 cursor-pointer ${
          isMonitorOpen
            ? "text-primary-container bg-primary-container/10 border border-primary-container/35 box-glow-cyan" 
            : "text-on-surface-variant hover:text-primary-fixed-dim"
        }`}
      >
        <span className="material-symbols-outlined text-[22px]">mic_external_on</span>
      </button>

      {/* Capture Screen Button */}
      <button
        onClick={onTriggerCapture}
        aria-label="Capture HUD Screen"
        className="text-on-surface-variant hover:text-primary-fixed-dim flex items-center justify-center w-11 h-11 rounded-full transition-all duration-300 hover:scale-110 active:scale-95 cursor-pointer hover:bg-primary-container/5"
      >
        <span className="material-symbols-outlined text-[22px]">photo_camera</span>
      </button>

    </nav>
  );
}
