import { useState, useEffect } from "react";

export default function Header() {
  const [time, setTime] = useState("");
  const [date, setDate] = useState("");
  
  // Real Hardware Indicators
  const [notificationCount, setNotificationCount] = useState(3);
  const [batteryLevel, setBatteryLevel] = useState("100%");
  const [batteryStatus, setBatteryStatus] = useState("BAT_OK");
  const [isCharging, setIsCharging] = useState(false);
  const [networkQuality, setNetworkQuality] = useState("98%");
  const [isOnline, setIsOnline] = useState(true);

  // Time & Date effect
  useEffect(() => {
    const updateDateTime = () => {
      const now = new Date();
      const hours = String(now.getHours()).padStart(2, "0");
      const minutes = String(now.getMinutes()).padStart(2, "0");
      const seconds = String(now.getSeconds()).padStart(2, "0");
      setTime(`${hours}:${minutes}:${seconds}`);

      const day = String(now.getDate()).padStart(2, "0");
      const month = String(now.getMonth() + 1).padStart(2, "0");
      const year = now.getFullYear();
      setDate(`${day}.${month}.${year}`);
    };

    updateDateTime();
    const interval = setInterval(updateDateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // Battery Status API
  useEffect(() => {
    if (typeof navigator.getBattery === "function") {
      navigator.getBattery().then((battery) => {
        const updateBatteryInfo = () => {
          const levelPercent = Math.round(battery.level * 100);
          setBatteryLevel(`${levelPercent}%`);
          setIsCharging(battery.charging);
          
          if (battery.charging) {
            setBatteryStatus("CHARGING");
          } else if (levelPercent < 20) {
            setBatteryStatus("BAT_LOW");
          } else {
            setBatteryStatus("BAT_OK");
          }
        };

        updateBatteryInfo();
        battery.addEventListener("levelchange", updateBatteryInfo);
        battery.addEventListener("chargingchange", updateBatteryInfo);

        return () => {
          battery.removeEventListener("levelchange", updateBatteryInfo);
          battery.removeEventListener("chargingchange", updateBatteryInfo);
        };
      });
    }
  }, []);

  // Network Status API
  useEffect(() => {
    const updateNetworkInfo = () => {
      setIsOnline(navigator.onLine);
      if (!navigator.onLine) {
        setNetworkQuality("DISCONN");
        return;
      }

      const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (conn) {
        // Estimate quality based on connection parameters
        const downlink = conn.downlink || 10;
        const type = conn.effectiveType || "4g";
        
        if (type === "4g" && downlink > 15) {
          setNetworkQuality("98% (4G)");
        } else if (type === "4g") {
          setNetworkQuality("85% (4G)");
        } else if (type === "3g") {
          setNetworkQuality("60% (3G)");
        } else {
          setNetworkQuality("30% (2G)");
        }
      } else {
        setNetworkQuality("ONLINE");
      }
    };

    updateNetworkInfo();
    window.addEventListener("online", updateNetworkInfo);
    window.addEventListener("offline", updateNetworkInfo);

    const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (conn) {
      conn.addEventListener("change", updateNetworkInfo);
    }

    return () => {
      window.removeEventListener("online", updateNetworkInfo);
      window.removeEventListener("offline", updateNetworkInfo);
      if (conn) {
        conn.removeEventListener("change", updateNetworkInfo);
      }
    };
  }, []);

  const isDesktop = !!window.electronAPI;

  return (
    <header className="fixed top-0 left-0 w-full bg-transparent text-primary font-mono text-[10px] border-b-[0.5px] border-primary-container/20 backdrop-blur-md flex justify-between items-center px-12 md:px-16 py-4 z-40 select-none draggable-header pointer-events-auto">
      {/* Branding & Status */}
      <div className="flex items-center gap-4 non-draggable">
        <span className="font-space text-lg font-bold tracking-tighter text-primary-fixed-dim drop-shadow-[0_0_8px_rgba(0,219,233,0.5)]">
          JARVIS_OS_v4.2
        </span>
        <span className="px-2 py-0.5 rounded border border-primary-container/30 bg-primary-container/5 text-primary-container text-[8px] animate-pulse uppercase tracking-widest font-medium">
          Online
        </span>
      </div>

      {/* Center Clock & Date */}
      <div className="hidden sm:flex items-center gap-8 text-[11px] font-semibold text-primary-container/85 non-draggable">
        <div className="flex items-center gap-2">
          <span className="text-primary/50 text-[9px] uppercase tracking-wider">Time:</span>
          <span className="text-glow-cyan font-mono tracking-widest">{time}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-primary/50 text-[9px] uppercase tracking-wider">Date:</span>
          <span className="font-mono tracking-widest">{date}</span>
        </div>
      </div>

      {/* Trailing Hardware Status Icons + Native Desktop Controls */}
      <div className="flex items-center gap-6 non-draggable">

        {/* Battery charging status icon */}
        <div 
          className="flex items-center gap-1.5 hover:text-primary-container transition-all cursor-pointer"
          title={`Battery Level: ${batteryLevel} (${batteryStatus})`}
        >
          <span className="material-symbols-outlined text-sm text-primary-container animate-pulse" style={{ fontVariationSettings: "'FILL' 1" }}>
            {isCharging ? "battery_charging_full" : "battery_full"}
          </span>
          <span className="text-[9px]">{batteryStatus === "CHARGING" ? `${batteryLevel} (${batteryStatus})` : `${batteryLevel} (${batteryStatus})`}</span>
        </div>

        {/* Electron Window Actions */}
        {isDesktop && (
          <div className="flex items-center gap-2 border-l border-primary-container/20 pl-4 ml-1">
            <button 
              onClick={() => window.electronAPI.minimizeApp()} 
              className="w-[18px] h-[18px] flex items-center justify-center rounded border border-primary-container/20 hover:border-primary-container/50 hover:bg-primary-container/15 text-primary-container text-[8px] active:scale-90 transition-all cursor-pointer"
              title="Minimize HUD"
            >
              —
            </button>
            <button 
              onClick={() => window.electronAPI.maximizeApp()} 
              className="w-[18px] h-[18px] flex items-center justify-center rounded border border-primary-container/20 hover:border-primary-container/50 hover:bg-primary-container/15 text-primary-container active:scale-90 transition-all cursor-pointer"
              title="Maximize HUD"
            >
              <span className="w-1.5 h-1.5 border border-primary-container/80 rounded-[1px]" />
            </button>
            <button 
              onClick={() => window.electronAPI.closeApp()} 
              className="w-[18px] h-[18px] flex items-center justify-center rounded border border-error/20 hover:border-error/50 hover:bg-error-container/25 text-error text-[8px] active:scale-90 transition-all cursor-pointer"
              title="Close HUD"
            >
              ✕
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
