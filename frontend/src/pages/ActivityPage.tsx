import React from 'react';
import { Activity, Clock } from 'lucide-react';
import { TasteShiftReplay } from '@/components/TasteShiftReplay';
import type { TasteEvent, RecommendationDecision } from '@/services/types';

export const ActivityPage: React.FC = () => {
  // Mock data for the activity timeline
  const mockEvents: { event: TasteEvent; decision?: RecommendationDecision }[] = [
    {
      event: {
        id: 'evt-1',
        user_id: 'u-1',
        type: 'feedback',
        created_at: new Date().toISOString(),
        taste_shift_vector: {
          spice_preference: 1.2,
          crunch_preference: 0.5
        }
      },
      decision: {
        id: 'dec-1',
        user_id: 'u-1',
        intent: 'Spicy dinner',
        context: {},
        recommended_dish_ids: ['d-101', 'd-102', 'd-103'],
        taste_profile_snapshot: {},
        created_at: new Date().toISOString()
      }
    },
    {
      event: {
        id: 'evt-2',
        user_id: 'u-1',
        type: 'order',
        created_at: new Date(Date.now() - 86400000).toISOString(),
        taste_shift_vector: {
          sweetness_preference: -0.8
        }
      }
    }
  ];

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 font-sans pb-28 selection:bg-orange-600/30">
      <header className="sticky top-0 z-30 bg-neutral-900/95 backdrop-blur-xl border-b border-neutral-800 px-4 py-3 shadow-xl">
        <div className="flex items-center gap-2">
          <Activity className="w-6 h-6 text-orange-400" />
          <h1 className="text-lg font-black text-white">Activity & Shifts</h1>
        </div>
      </header>

      <main className="max-w-2xl mx-auto p-4 pt-6 space-y-6">
        <div className="flex items-center gap-2 mb-2">
          <Clock className="w-5 h-5 text-neutral-400" />
          <h2 className="text-sm font-bold text-neutral-300">Timeline</h2>
        </div>

        <div className="border-l-2 border-neutral-800 pl-4 space-y-6 relative ml-2">
          {mockEvents.map((item) => (
            <div key={item.event.id} className="relative">
              <div className="absolute -left-[23px] top-4 w-3 h-3 rounded-full bg-orange-500 border-2 border-neutral-950" />
              <TasteShiftReplay event={item.event} decision={item.decision} />
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};
