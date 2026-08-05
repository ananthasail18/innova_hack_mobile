import React from 'react';
import { NavLink } from 'react-router-dom';
import { Utensils, Sparkles, Bot, Activity } from 'lucide-react';

interface MobileBottomNavProps {
  isPhoneFrame?: boolean;
}

export const MobileBottomNav: React.FC<MobileBottomNavProps> = ({ isPhoneFrame = false }) => {

  const navItems = [
    { to: '/restaurant', icon: Utensils, label: 'Discover' },
    { to: '/assistant', icon: Bot, label: 'Assistant' },
    { to: '/taste-dna', icon: Sparkles, label: 'Taste Passport' },
    { to: '/activity', icon: Activity, label: 'Activity' },
  ];

  const containerPosition = isPhoneFrame 
    ? 'absolute bottom-2 left-3 right-3 z-40' 
    : 'fixed bottom-2 left-3 right-3 max-w-lg mx-auto z-40';

  return (
    <nav 
      aria-label="Mobile Bottom Navigation" 
      className={`${containerPosition} bg-neutral-900/90 backdrop-blur-xl border border-neutral-800/80 rounded-2xl shadow-[0_12px_32px_rgba(0,0,0,0.8)] px-2 py-1.5`}
    >
      <div className="flex items-center justify-around h-14">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex flex-col items-center justify-center flex-1 h-full py-1 text-[10px] font-bold rounded-xl transition-all duration-300 relative ${
                  isActive 
                    ? 'text-orange-400 bg-orange-500/15 border border-orange-500/30 scale-105 shadow-inner' 
                    : 'text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800/40'
                }`
              }
            >
              <div className="relative">
                <Icon className="w-4 h-4 mb-0.5" />
              </div>
              <span className="tracking-tight">{item.label}</span>
            </NavLink>
          );
        })}
      </div>
    </nav>
  );
};
