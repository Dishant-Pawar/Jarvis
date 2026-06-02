import { useEffect, useRef, useState } from "react";

export default function CustomCursor({ isEnabled }) {
  const cursorOuterRef = useRef(null);
  const cursorInnerRef = useRef(null);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    if (!isEnabled) {
      document.body.classList.remove("custom-cursor-active");
      return;
    }

    document.body.classList.add("custom-cursor-active");

    const mousePos = { x: -100, y: -100 };
    const outerPos = { x: -100, y: -100 };
    let animationFrameId = null;

    const onMouseMove = (e) => {
      mousePos.x = e.clientX;
      mousePos.y = e.clientY;
    };

    const updateCursor = () => {
      // Smooth interpolation for the outer ring
      const ease = 0.15;
      outerPos.x += (mousePos.x - outerPos.x) * ease;
      outerPos.y += (mousePos.y - outerPos.y) * ease;

      if (cursorInnerRef.current) {
        cursorInnerRef.current.style.left = `${mousePos.x}px`;
        cursorInnerRef.current.style.top = `${mousePos.y}px`;
      }

      if (cursorOuterRef.current) {
        cursorOuterRef.current.style.left = `${outerPos.x}px`;
        cursorOuterRef.current.style.top = `${outerPos.y}px`;
      }

      animationFrameId = requestAnimationFrame(updateCursor);
    };

    const handleMouseOver = (e) => {
      // Detect if cursor is hovering over interactive elements
      const target = e.target;
      const isInteractive = 
        target.tagName === "BUTTON" || 
        target.tagName === "A" || 
        target.closest("button") || 
        target.closest("a") || 
        target.closest(".interactive-hover");
      
      setIsHovered(!!isInteractive);
    };

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseover", handleMouseOver);
    animationFrameId = requestAnimationFrame(updateCursor);

    return () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseover", handleMouseOver);
      cancelAnimationFrame(animationFrameId);
      document.body.classList.remove("custom-cursor-active");
    };
  }, [isEnabled]);

  if (!isEnabled) return null;

  return (
    <>
      {/* Outer reticle ring */}
      <div
        ref={cursorOuterRef}
        className={`fixed w-7 h-7 rounded-full border border-primary-fixed-dim/50 pointer-events-none z-[9999] -translate-x-1/2 -translate-y-1/2 mix-blend-screen transition-transform duration-200 ease-out shadow-[0_0_8px_rgba(0,219,233,0.3)] ${
          isHovered ? "scale-150 border-primary-container bg-primary-container/10" : ""
        }`}
      />
      {/* Inner precise dot */}
      <div
        ref={cursorInnerRef}
        className="fixed w-1.5 h-1.5 bg-primary-container rounded-full pointer-events-none z-[9999] -translate-x-1/2 -translate-y-1/2 mix-blend-screen shadow-[0_0_4px_rgba(0,219,233,1)]"
      />
    </>
  );
}
