import React, { useState } from 'react';
import { ZomatoDishBadge } from '@/components/ZomatoDishBadge'; // We can leave this component name or rename it later
import { 
  Sparkles, 
  ArrowLeft, 
  Star, 
  Clock, 
  MapPin, 
  Search, 
  ShoppingCart, 
  CheckCircle, 
  Flame, 
  Plus, 
  ThumbsUp,
  AlertTriangle
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '@/hooks/useCart';
import type { Dish } from '@/services/types';

interface SandboxDish {
  id: string;
  name: string;
  price: number;
  description: string;
  category: string;
  matchScore: number;
  reason: string;
  isVeg: boolean;
  image: string;
  mustTry?: boolean;
  votes: number;
  rating: number;
}

const CLONED_MARKETPLACE_DISHES: SandboxDish[] = [
  {
    id: 'mp-1',
    name: 'Spicy Garlic Butter Noodles',
    price: 345,
    description: 'Wok-tossed fresh noodles infused with roasted garlic butter, red chili oil, scallions, and toasted sesame.',
    category: 'Indo-Chinese',
    matchScore: 96,
    reason: 'High Spice (8.5/10) & Crunchiness matches your 8D Taste DNA profile.',
    isVeg: true,
    image: '/images/dishes/spicy_noodles.jpg',
    mustTry: true,
    votes: 42,
    rating: 4.8,
  },
  {
    id: 'mp-2',
    name: 'Cheesy Gourmet Burger & Fries',
    price: 420,
    description: 'Double melted cheddar patty topped with caramelized onions, crisp pickles, and special house sauce.',
    category: 'Burgers',
    matchScore: 91,
    reason: 'Matches your Creaminess (7/10) & Masala Intensity preferences.',
    isVeg: false,
    image: '/images/dishes/burger.jpg',
    mustTry: true,
    votes: 89,
    rating: 4.7,
  },
  {
    id: 'mp-3',
    name: 'Crispy Paneer Pepper Fry',
    price: 310,
    description: 'Golden paneer cubes wok-tossed with crushed Tellicherry black pepper, curry leaves, and green chilies.',
    category: 'Starters',
    matchScore: 88,
    reason: 'High Masala Intensity & Crispiness level matched.',
    isVeg: true,
    image: '/images/dishes/paneer_fry.jpg',
    mustTry: true,
    votes: 28,
    rating: 4.6,
  },
  {
    id: 'mp-4',
    name: 'Classic Butter Chicken & Naan',
    price: 450,
    description: 'Slow-cooked tandoori chicken pieces simmered in rich velvety tomato butter gravy with garlic naan.',
    category: 'Main Course',
    matchScore: 84,
    reason: 'Rich Creaminess & Tangy tomato notes matched.',
    isVeg: false,
    image: '/images/dishes/butter_chicken.jpg',
    mustTry: false,
    votes: 112,
    rating: 4.9,
  },
  {
    id: 'mp-5',
    name: 'Sizzling Chocolate Brownie Sundae',
    price: 260,
    description: 'Warm fudge brownie served on a sizzling hot plate topped with vanilla bean ice cream and chocolate drizzle.',
    category: 'Desserts',
    matchScore: 68,
    reason: 'Sweetness preference matched.',
    isVeg: true,
    image: '/images/dishes/brownie.jpg',
    mustTry: false,
    votes: 56,
    rating: 4.5,
  },
];

export const MarketplaceSandboxPage: React.FC = () => {
  const navigate = useNavigate();
  const { addItem, totalItems } = useCart();
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [addedItemIds, setAddedItemIds] = useState<Record<string, boolean>>({});

  const categories = ['All', 'Indo-Chinese', 'Burgers', 'Starters', 'Main Course', 'Desserts'];

  const filteredDishes = CLONED_MARKETPLACE_DISHES.filter((dish) => {
    const matchesCategory = selectedCategory === 'All' || dish.category === selectedCategory;
    const matchesSearch = dish.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          dish.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const handleAddToCart = (mDish: SandboxDish) => {
    const compliantDish: Dish = {
      id: mDish.id,
      restaurant_id: 'r1',
      category_id: 'c1',
      name: mDish.name,
      description: mDish.description,
      price: mDish.price,
      image_url: mDish.image,
      is_vegetarian: mDish.isVeg,
      is_available: true,
      display_order: 1,
      spice_level: 5,
      sweetness_level: 5,
      creaminess_level: 5,
      tanginess_level: 5,
      masala_intensity_level: 5,
      crunchiness_level: 5,
      oiliness_level: 5,
      saltiness_level: 5,
      ingredients: [],
      allergens: [],
      dietary_tags: [],
      recommended_pairings: [],
      preparation_style: null,
      chef_notes: null,
      serving_style: null,
      recommended_temperature: null,
      popularity_score: 95,
    };

    addItem(compliantDish, 1);
    setAddedItemIds((prev) => ({ ...prev, [mDish.id]: true }));
    setTimeout(() => {
      setAddedItemIds((prev) => ({ ...prev, [mDish.id]: false }));
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 font-sans pb-28 selection:bg-indigo-600/30">
      
      {/* Banner */}
      <div className="bg-indigo-600 text-white text-xs font-bold px-2 py-1.5 flex items-center justify-center gap-2">
        <AlertTriangle className="w-4 h-4" />
        <span>Simulated marketplace integration sandbox</span>
      </div>

      {/* Header */}
      <header className="sticky top-0 z-30 bg-neutral-900/95 backdrop-blur-xl border-b border-neutral-800 px-3.5 py-2.5 shadow-xl flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button 
            onClick={() => navigate(-1)} 
            className="p-1 rounded-full text-neutral-400 hover:text-white hover:bg-neutral-800 transition-all"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          
          <div className="flex items-center gap-1.5">
            <span className="text-indigo-400 font-black text-base tracking-tighter">MARKETPLACE</span>
          </div>
        </div>

        {/* TasteAI Active Overlay Badge */}
        <div className="flex items-center gap-1.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 px-2.5 py-1 rounded-full text-white text-[10px] font-black shadow-md shadow-indigo-950/50 animate-pulse">
          <Sparkles className="w-3 h-3 text-yellow-300 fill-yellow-300" />
          <span>TasteAI Active</span>
        </div>

        {/* Cart Shortcut */}
        <button 
          onClick={() => navigate('/cart')} 
          className="relative p-1.5 text-neutral-300 hover:text-white"
        >
          <ShoppingCart className="w-5 h-5" />
          {totalItems > 0 && (
            <span className="absolute -top-1 -right-1 bg-indigo-600 text-white text-[9px] font-black px-1.5 py-0.2 rounded-full min-w-[16px] text-center shadow-md">
              {totalItems}
            </span>
          )}
        </button>
      </header>

      {/* Partner Restaurant Header Banner */}
      <section className="bg-gradient-to-b from-neutral-900 via-neutral-900/90 to-neutral-950 border-b border-neutral-800/80 px-4 pt-4 pb-5">
        <div className="max-w-4xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="bg-indigo-600 text-white text-[9px] font-black px-2 py-0.5 rounded uppercase tracking-wider shadow-sm">
                PREMIUM PARTNER
              </span>
              <span className="text-xs text-neutral-400 font-medium">• Koramangala 5th Block</span>
            </div>

            <h1 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
              <span>Truffles</span>
              <Flame className="w-5 h-5 text-orange-500 fill-orange-500" />
            </h1>
            <p className="text-neutral-400 text-xs mt-1">American Burgers, Indo-Chinese, Fast Food, Desserts</p>

            <div className="flex items-center gap-3 text-xs text-neutral-400 mt-3">
              <span className="flex items-center gap-1 text-emerald-400 font-bold bg-emerald-950/90 border border-emerald-800/60 px-2 py-0.5 rounded-lg shadow-sm">
                <Star className="w-3.5 h-3.5 fill-emerald-400" /> 4.6 (14.8k+)
              </span>
              <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5 text-neutral-500" /> 25 mins</span>
              <span className="flex items-center gap-1"><MapPin className="w-3.5 h-3.5 text-neutral-500" /> 1.8 km</span>
            </div>
          </div>

          {/* Taste DNA Active Profile Card */}
          <div className="bg-neutral-900/90 border border-indigo-500/30 rounded-2xl p-3.5 flex items-center gap-3 shadow-lg backdrop-blur-md">
            <div className="p-2.5 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl text-white shadow-md">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <div className="text-[10px] uppercase tracking-wider text-indigo-400 font-bold">Matching Diner DNA</div>
              <div className="text-sm font-black text-white">Ananth's 8D Taste Vector</div>
              <div className="text-[10px] text-neutral-400 mt-0.5">High Spice • High Crunch • Creamy Gravy</div>
            </div>
          </div>
        </div>
      </section>

      {/* Category Tabs & Search Bar */}
      <section className="max-w-4xl mx-auto px-4 py-2 space-y-3 mt-4">
        <div className="flex items-center gap-2 bg-neutral-900/90 border border-neutral-800 rounded-xl px-3 py-2 shadow-inner">
          <Search className="w-4 h-4 text-neutral-500" />
          <input
            type="text"
            placeholder="Search menu items..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="bg-transparent text-xs text-neutral-200 placeholder-neutral-500 outline-none w-full"
          />
        </div>

        {/* Scrollable Category Filter Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 no-scrollbar">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-extrabold whitespace-nowrap transition-all ${
                selectedCategory === cat
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-950 scale-105'
                  : 'bg-neutral-900 text-neutral-400 border border-neutral-800 hover:text-neutral-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </section>

      {/* Cloned Food Item Product Cards */}
      <main className="max-w-4xl mx-auto px-4 space-y-3.5 pt-2 mt-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-black text-neutral-400 uppercase tracking-widest flex items-center gap-1.5">
            <span>RECOMMENDED MENU ITEMS</span>
            <span className="text-[10px] text-neutral-500">({filteredDishes.length})</span>
          </h2>
          <span className="text-[11px] text-indigo-400 font-bold flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-indigo-400" /> Ranked by 8D Taste DNA
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          {filteredDishes.map((dish) => (
            <div 
              key={dish.id} 
              className="bg-neutral-900/90 border border-neutral-800/90 hover:border-indigo-500/40 rounded-2xl p-3.5 flex items-start justify-between gap-3 relative overflow-hidden transition-all shadow-lg backdrop-blur-sm"
            >
              <div className="flex-1 space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className={`w-3.5 h-3.5 border flex items-center justify-center p-0.5 rounded-sm ${dish.isVeg ? 'border-emerald-500' : 'border-red-500'}`}>
                    <span className={`w-1.5 h-1.5 rounded-full ${dish.isVeg ? 'bg-emerald-500' : 'bg-red-500'}`} />
                  </span>
                  
                  <h3 className="font-extrabold text-sm text-neutral-100">{dish.name}</h3>

                  {dish.mustTry && (
                    <span className="text-[8px] font-black bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 px-1 py-0.2 rounded uppercase">
                      MUST TRY
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-2 text-[11px] text-neutral-400">
                  <span className="flex items-center gap-0.5 text-amber-400 font-bold">
                    <Star className="w-3 h-3 fill-amber-400 text-amber-400" /> {dish.rating}
                  </span>
                  <span className="flex items-center gap-1 text-neutral-500">
                    <ThumbsUp className="w-3 h-3" /> {dish.votes} votes
                  </span>
                </div>

                <div className="text-sm font-black text-neutral-100">₹{dish.price}</div>

                <p className="text-[11px] text-neutral-400 line-clamp-2 leading-relaxed">{dish.description}</p>

                <div className="bg-neutral-950/90 border border-indigo-500/30 rounded-xl p-2 text-[10px] text-neutral-300 flex items-start gap-1.5 mt-1">
                  <Sparkles className="w-3.5 h-3.5 text-indigo-400 shrink-0 mt-0.5" />
                  <span>{dish.reason}</span>
                </div>
              </div>

              <div className="w-24 shrink-0 flex flex-col items-center gap-2 relative">
                <div className="w-24 h-24 rounded-xl overflow-hidden bg-neutral-950 border border-neutral-800 relative">
                  <img 
                    src={dish.image} 
                    alt={dish.name} 
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = '/images/dishes/spicy_noodles.jpg';
                    }}
                  />
                  
                  <div className="absolute top-1 right-1">
                    <ZomatoDishBadge matchPercentage={dish.matchScore} size="sm" />
                  </div>
                </div>

                <button
                  onClick={() => handleAddToCart(dish)}
                  className={`w-full py-1.5 rounded-xl text-xs font-black flex items-center justify-center gap-1 transition-all shadow-md ${
                    addedItemIds[dish.id]
                      ? 'bg-emerald-600 text-white shadow-emerald-950'
                      : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-indigo-950 active:scale-95'
                  }`}
                >
                  {addedItemIds[dish.id] ? (
                    <>
                      <CheckCircle className="w-3.5 h-3.5" /> Added
                    </>
                  ) : (
                    <>
                      <Plus className="w-3.5 h-3.5" /> ADD +
                    </>
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};
