import React from 'react';
import { Bot, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const AssistantPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 font-sans pb-28">
      <header className="sticky top-0 z-30 bg-neutral-900/95 backdrop-blur-xl border-b border-neutral-800 px-4 py-3 shadow-xl">
        <div className="flex items-center gap-2">
          <Bot className="w-6 h-6 text-orange-400" />
          <h1 className="text-lg font-black text-white">TasteAI Assistant</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto p-4 flex flex-col items-center justify-center min-h-[60vh] text-center">
        <div className="p-4 bg-orange-500/10 rounded-full mb-4">
          <Sparkles className="w-12 h-12 text-orange-500" />
        </div>
        <h2 className="text-2xl font-black mb-2">How can I help you?</h2>
        <p className="text-neutral-400 mb-6 max-w-md">
          I can help you discover dishes matching your Taste DNA or suggest restaurants based on your current mood.
        </p>
        <button 
          onClick={() => navigate('/restaurant')}
          className="bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 px-6 rounded-xl transition-all"
        >
          Explore Menu
        </button>
      </main>
    </div>
  );
};
