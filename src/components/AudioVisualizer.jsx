import { useState, useEffect } from "react";

export default function AudioVisualizer({ isActive }) {
  const [heights, setHeights] = useState(Array(18).fill(4));

  useEffect(() => {
    if (!isActive) {
      setHeights(Array(18).fill(4));
      return;
    }

    const interval = setInterval(() => {
      setHeights(
        Array(18)
          .fill(0)
          .map(() => Math.max(6, Math.min(48, Math.round(Math.random() * 50))))
      );
    }, 100);

    return () => clearInterval(interval);
  }, [isActive]);

  if (!isActive) return null;

  return (
    <div className="fixed bottom-28 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3 z-30 select-none pointer-events-none">
      
      {/* Waveform Bars Container */}
      <div className="flex items-center justify-center gap-[3px] h-14 w-[180px] px-4 rounded-full border border-primary-container/10 bg-black/25 backdrop-blur-lg shadow-[0_0_20px_rgba(0,219,233,0.08)]">
        {heights.map((h, idx) => (
          <div
            key={idx}
            className="w-[3px] bg-primary-container rounded-full transition-all duration-100 ease-in-out shadow-[0_0_8px_rgba(0,219,233,0.5)]"
            style={{
              height: `${h}px`,
              // Symmetry visual effect
              opacity: 0.3 + (idx < 9 ? idx / 12 : (17 - idx) / 12),
            }}
          />
        ))}
      </div>

      {/* Voice Status Sub-text */}
      <span className="font-mono text-[8px] text-primary-container/90 uppercase tracking-[0.2em] font-semibold animate-pulse text-glow-cyan">
        listening_vocal_synthesizer...
      </span>
    </div>
  );
}
