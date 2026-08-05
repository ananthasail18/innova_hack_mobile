import type { DishRecommendation, RecommendationIntent, AssistantResult } from './types';
import { offlineStore } from './offlineStore';

export class LocalRecommendationEngine {
  static getRecommendations(intent: RecommendationIntent): AssistantResult {
    const dishes = offlineStore.getCatalog();
    const profile = offlineStore.getProfile();
    
    if (!profile) {
      return {
        message: "You are offline and no taste profile is cached. Please connect to the internet to get personalized recommendations.",
        recommendations: [],
        source: 'DEVICE_OFFLINE'
      };
    }

    if (dishes.length === 0) {
      return {
        message: "You are offline and no menu is cached. We couldn't find any dishes.",
        recommendations: [],
        source: 'DEVICE_OFFLINE'
      };
    }

    let scoredDishes: DishRecommendation[] = dishes.map(dish => {
      // Basic euclidean-like distance logic for offline deterministic engine
      const spiceDiff = Math.abs(dish.spice_level - profile.spice_preference);
      const sweetDiff = Math.abs(dish.sweetness_level - profile.sweetness_preference);
      const crunchDiff = Math.abs(dish.crunchiness_level - profile.crunchiness_preference);
      
      let score = 100 - ((spiceDiff + sweetDiff + crunchDiff) * 5);
      
      if (intent.filters?.is_vegetarian && !dish.is_vegetarian) {
        score = -1; // filter out
      }

      return {
        dish,
        score: Math.max(0, Math.min(100, score)),
        confidence: score > 80 ? 0.9 : 0.6,
        reasons: [{ type: 'match', text: 'Matched via offline deterministic engine.' }]
      };
    });

    // Filter and sort top 5
    scoredDishes = scoredDishes
      .filter(d => d.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 5);

    return {
      message: `Here are ${scoredDishes.length} recommendations generated offline based on your Taste Passport.`,
      recommendations: scoredDishes,
      source: 'DEVICE_OFFLINE'
    };
  }
}
