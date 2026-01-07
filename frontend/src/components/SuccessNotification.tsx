/**
 * SuccessNotification Component
 * Shows animated success message for correct quiz answers
 */
'use client';

import { useEffect, useState } from 'react';

interface SuccessNotificationProps {
  show: boolean;
  onHide: () => void;
}

export default function SuccessNotification({ show, onHide }: SuccessNotificationProps) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (show) {
      setVisible(true);
      const timer = setTimeout(() => {
        setVisible(false);
        setTimeout(onHide, 300);
      }, 2500);
      return () => clearTimeout(timer);
    }
  }, [show, onHide]);

  if (!show && !visible) return null;

  return (
    <>
      {/* Confetti explosion from message area */}
      <div className={`confetti-explosion ${visible ? 'active' : ''}`}>
        {[...Array(80)].map((_, i) => {
          const colors = ['#10b981', '#34d399', '#6ee7b7', '#fbbf24', '#f59e0b', '#60a5fa', '#ec4899', '#8b5cf6'];
          return (
            <div 
              key={i} 
              className="confetti-particle" 
              style={{
                left: `${20 + Math.random() * 60}%`,
                animationDelay: `${Math.random() * 0.3}s`,
                backgroundColor: colors[i % colors.length],
                '--rotation': `${Math.random() * 720}deg`,
              } as React.CSSProperties}
            />
          );
        })}
      </div>

      {/* Sparkle effects */}
      <div className={`sparkles ${visible ? 'active' : ''}`}>
        {[...Array(20)].map((_, i) => (
          <div 
            key={i} 
            className="sparkle" 
            style={{
              left: `${Math.random() * 100}%`,
              top: `${30 + Math.random() * 40}%`,
              animationDelay: `${Math.random() * 0.5}s`,
            }}
          >
            ★
          </div>
        ))}
      </div>
    </>
  );
}
