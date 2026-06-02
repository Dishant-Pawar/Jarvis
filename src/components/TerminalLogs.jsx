import { useState, useEffect, useRef } from "react";

const INITIAL_LOGS = [
  "[SYSTEM] JARVIS v4.2 Kernel Loaded Successfully.",
  "[SYSTEM] Loading network interface config...",
  "[SYSTEM] Network connected (IP: 192.168.1.104).",
  "[SECURITY] Decryption keys verification: SUCCESS.",
  "[CORE] CPU temperature: 42°C | GPU temperature: 38°C",
  "[AI_ENGINE] Neural synapse connection established.",
  "[AI_ENGINE] Listening on default microphone interface...",
  "[SYSTEM] Ready for user query input."
];

const DIAGNOSTICS_LOGS = [
  "[DIAG] Starting full core stack evaluation...",
  "[DIAG] Testing CPU registers... PASS",
  "[DIAG] Testing GPU graphic pipeline... PASS",
  "[DIAG] Measuring RAM write-read cycles (32GB)... PASS",
  "[DIAG] Analyzing neural network latency... 12ms",
  "[DIAG] Checksum node 0x8F9A2B... OK",
  "[DIAG] Checksum node 0x4C3D2E... OK",
  "[DIAG] Checking biometric encryption keys... APPROVED",
  "[DIAG] Battery charge capacity... 100% HEALTHY",
  "[DIAG] All auxiliary operations: NOMINAL.",
  "[DIAG] Diagnostics complete. Code: 0x000"
];

const DUMMY_LIVE_LOGS = [
  "[SYSTEM] Core memory cleaning: freed 4.2 MB cache.",
  "[AI_ENGINE] Refreshing dialogue context graph...",
  "[CORE] Thermal sensor feedback: fan speed adjusted to 45%.",
  "[SECURITY] Firewall scan completed: 0 threats detected.",
  "[SYSTEM] Syncing localized system state to cloud storage...",
  "[NETWORK] Latency check: ping to primary server 14ms.",
  "[CORE] Main voltage level stabilized at 1.25V."
];

export default function TerminalLogs({ isDiagnosticsRunning, onDiagnosticsComplete, newLogs = [] }) {
  const [logs, setLogs] = useState(INITIAL_LOGS);
  const terminalEndRef = useRef(null);

  // Handle external logs injection from backend operations
  useEffect(() => {
    if (newLogs && newLogs.length > 0) {
      const lastLog = newLogs[newLogs.length - 1];
      setLogs((prev) => [...prev, lastLog]);
    }
  }, [newLogs]);

  // Auto-scroll logs
  useEffect(() => {
    if (terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  // Periodic random logs simulator
  useEffect(() => {
    if (isDiagnosticsRunning) return; // Wait during diagnostics

    const interval = setInterval(() => {
      const randomLog = DUMMY_LIVE_LOGS[Math.floor(Math.random() * DUMMY_LIVE_LOGS.length)];
      const timestamp = new Date().toLocaleTimeString();
      setLogs((prev) => [...prev, `[${timestamp}] ${randomLog}`]);
    }, 4500);

    return () => clearInterval(interval);
  }, [isDiagnosticsRunning]);

  // Run diagnostics sequence
  useEffect(() => {
    if (!isDiagnosticsRunning) return;

    // Reset logs or prepend diagnostics header
    setLogs((prev) => [...prev, `\n--- RUNNING DIAGNOSTICS SEQUENCE ---\n`]);

    let logIndex = 0;
    const interval = setInterval(() => {
      if (logIndex < DIAGNOSTICS_LOGS.length) {
        setLogs((prev) => [...prev, DIAGNOSTICS_LOGS[logIndex]]);
        logIndex++;
      } else {
        clearInterval(interval);
        onDiagnosticsComplete(); // Signal completion
      }
    }, 400);

    return () => clearInterval(interval);
  }, [isDiagnosticsRunning]);

  return (
    <div className="fixed left-margin-desktop bottom-28 w-[340px] md:w-[400px] h-[220px] glass-panel rounded-xl p-4 flex flex-col z-30 pointer-events-auto select-none">
      {/* Console Header */}
      <div className="flex justify-between items-center border-b border-primary-container/10 pb-2 mb-2 font-mono text-[10px] tracking-wider text-primary-fixed-dim/80">
        <div className="flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-primary-container animate-pulse" />
          <span>SYS_DIAG_TERMINAL</span>
        </div>
        <button 
          onClick={() => setLogs(INITIAL_LOGS)}
          className="text-[9px] text-primary/40 hover:text-primary-container transition-colors"
          title="Clear console"
        >
          CLEAR
        </button>
      </div>

      {/* Console Output Area */}
      <div className="flex-1 overflow-y-auto custom-scrollbar pr-1 font-mono text-[9px] leading-relaxed text-primary/80 flex flex-col gap-1">
        {logs.map((log, idx) => {
          let styleClass = "";
          if (log.includes("[DIAG]")) {
            styleClass = "text-primary-fixed-dim font-medium";
          } else if (log.includes("[SYSTEM]")) {
            styleClass = "text-secondary-fixed-dim";
          } else if (log.includes("[SECURITY]")) {
            styleClass = "text-tertiary-container";
          } else if (log.includes("---")) {
            styleClass = "text-primary-container font-semibold text-center";
          }
          
          return (
            <div key={idx} className={`whitespace-pre-wrap ${styleClass}`}>
              {log}
            </div>
          );
        })}
        <div ref={terminalEndRef} />
      </div>
    </div>
  );
}
