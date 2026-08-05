import React from 'react';
import type { TasteEvent, RecommendationDecision } from '@/services/types';
import { ArrowRight, Flame, Droplet, Cookie, Zap } from 'lucide-react';

interface TasteShiftReplayProps {
  event: TasteEvent;
  decision?: RecommendationDecision;
}

export const TasteShiftReplay: React.FC<TasteShiftReplayProps> = ({ event, decision }) => {
  // A simple visualizer of how their Taste DNA shifted
  
  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-4 mb-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-bold text-white flex items-center gap-2">
          <Zap className="w-4 h-4 text-orange-400" /> Taste DNA Shift Replay
        </h3>
        <span className="text-xs text-neutral-500">{new Date(event.created_at).toLocaleDateString()}</span>
      </div>
      
      <p className="text-xs text-neutral-400 mb-4">
        {event.type === 'feedback' ? "Based on your recent feedback, your profile shifted:" : "Your preferences evolved after your last order:"}
      </p>

      <div className="space-y-3">
        {event.taste_shift_vector?.spice_preference !== undefined && (
          <div className="flex items-center justify-between text-xs">
            <span className="text-neutral-300 flex items-center gap-1.5 w-24">
              <Flame className="w-3.5 h-3.5 text-red-500" /> Spice
            </span>
            <div className="flex-1 flex items-center gap-2 px-2">
              <div className="h-1.5 flex-1 bg-neutral-800 rounded-full overflow-hidden">
                <div className="h-full bg-red-600 rounded-full" style={{ width: '40%' }}></div>
              </div>
              <ArrowRight className="w-3 h-3 text-neutral-500" />
              <div className="h-1.5 flex-1 bg-neutral-800 rounded-full overflow-hidden relative">
                <div className="h-full bg-red-500 rounded-full shadow-[0_0_8px_rgba(239,68,68,0.8)]" style={{ width: `${event.taste_shift_vector.spice_preference * 10}%` }}></div>
              </div>
            </div>
            <span className="w-8 text-right font-bold text-red-400">+{event.taste_shift_vector.spice_preference}</span>
          </div>
        )}
        
        {event.taste_shift_vector?.sweetness_preference !== undefined && (
          <div className="flex items-center justify-between text-xs">
            <span className="text-neutral-300 flex items-center gap-1.5 w-24">
              <Droplet className="w-3.5 h-3.5 text-amber-500" /> Sweetness
            </span>
            <div className="flex-1 flex items-center gap-2 px-2">
              <div className="h-1.5 flex-1 bg-neutral-800 rounded-full overflow-hidden">
                <div className="h-full bg-amber-600 rounded-full" style={{ width: '60%' }}></div>
              </div>
              <ArrowRight className="w-3 h-3 text-neutral-500" />
              <div className="h-1.5 flex-1 bg-neutral-800 rounded-full overflow-hidden relative">
                <div className="h-full bg-amber-500 rounded-full shadow-[0_0_8px_rgba(245,158,11,0.8)]" style={{ width: `${event.taste_shift_vector.sweetness_preference * 10}%` }}></div>
              </div>
            </div>
            <span className="w-8 text-right font-bold text-amber-400">{event.taste_shift_vector.sweetness_preference}</span>
          </div>
        )}

        {event.taste_shift_vector?.crunch_preference !== undefined && (
          <div className="flex items-center justify-between text-xs">
            <span className="text-neutral-300 flex items-center gap-1.5 w-24">
              <Cookie className="w-3.5 h-3.5 text-yellow-600" /> Crunch
            </span>
            <div className="flex-1 flex items-center gap-2 px-2">
              <div className="h-1.5 flex-1 bg-neutral-800 rounded-full overflow-hidden">
                <div className="h-full bg-yellow-700 rounded-full" style={{ width: '50%' }}></div>
              </div>
              <ArrowRight className="w-3 h-3 text-neutral-500" />
              <div className="h-1.5 flex-1 bg-neutral-800 rounded-full overflow-hidden relative">
                <div className="h-full bg-yellow-600 rounded-full shadow-[0_0_8px_rgba(202,138,4,0.8)]" style={{ width: `${event.taste_shift_vector.crunch_preference * 10}%` }}></div>
              </div>
            </div>
            <span className="w-8 text-right font-bold text-yellow-500">+{event.taste_shift_vector.crunch_preference}</span>
          </div>
        )}
      </div>

      {decision && (
        <div className="mt-4 pt-3 border-t border-neutral-800">
          <p className="text-[10px] text-neutral-500 uppercase tracking-wider mb-1">Rankings adjusted for:</p>
          <div className="flex flex-wrap gap-1.5">
            {decision.recommended_dish_ids.slice(0, 3).map(id => (
              <span key={id} className="text-[10px] bg-neutral-800 px-2 py-0.5 rounded text-neutral-300">Dish #{id}</span>
            ))}
            {decision.recommended_dish_ids.length > 3 && (
              <span className="text-[10px] text-neutral-500">+{decision.recommended_dish_ids.length - 3} more</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
