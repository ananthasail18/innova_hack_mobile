import math
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.taste_profile import TasteProfile
from app.models.dish import Dish
from app.models.restaurant import Restaurant
from app.models.community_signal import CommunitySignal
from app.schemas.recommendation import DishRecommendation, RecommendationReason, RecommendationResponse
from app.schemas.dish import DishOut
from app.schemas.ai import RecommendationIntent

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def _get_taste_vector(self, obj) -> List[float]:
        return [
            float(obj.spice_preference if hasattr(obj, 'spice_preference') else obj.spice_level),
            float(obj.sweetness_preference if hasattr(obj, 'sweetness_preference') else obj.sweetness_level),
            float(obj.creaminess_preference if hasattr(obj, 'creaminess_preference') else obj.creaminess_level),
            float(obj.tanginess_preference if hasattr(obj, 'tanginess_preference') else obj.tanginess_level),
            float(obj.masala_intensity_preference if hasattr(obj, 'masala_intensity_preference') else obj.masala_intensity_level),
            float(obj.crunchiness_preference if hasattr(obj, 'crunchiness_preference') else obj.crunchiness_level),
            float(obj.oiliness_preference if hasattr(obj, 'oiliness_preference') else obj.oiliness_level),
            float(obj.saltiness_preference if hasattr(obj, 'saltiness_preference') else obj.saltiness_level)
        ]

    def _get_community_score(self, user_id: str, dish_id: str, user_taste_vector: List[float]) -> float:
        # Find other users' signals for this dish
        signals = self.db.query(CommunitySignal).filter(CommunitySignal.dish_id == dish_id, CommunitySignal.user_id != user_id).all()
        if not signals:
            return 0.0
            
        # Get their taste profiles
        other_user_ids = [s.user_id for s in signals]
        other_profiles = self.db.query(TasteProfile).filter(TasteProfile.user_id.in_(other_user_ids)).all()
        
        profile_map = {p.user_id: p for p in other_profiles}
        
        score_sum = 0.0
        weight_sum = 0.0
        
        for signal in signals:
            if signal.user_id not in profile_map:
                continue
                
            other_vector = self._get_taste_vector(profile_map[signal.user_id])
            sim = cosine_similarity(user_taste_vector, other_vector)
            
            # Only consider users with similar taste (> 0.82)
            if sim > 0.82:
                # signal weight: liked is positive, rating can be scaled
                item_score = 0.0
                if signal.liked: item_score += 0.5
                if signal.would_reorder: item_score += 0.5
                
                score_sum += item_score * sim
                weight_sum += sim
                
        if weight_sum == 0:
            return 0.0
            
        return score_sum / weight_sum

    def get_recommendations(self, user_id: str, restaurant_id: str = None, intent: RecommendationIntent = None) -> RecommendationResponse:
        user_profile = self.db.query(TasteProfile).filter(TasteProfile.user_id == user_id).first()
        if not user_profile:
            # Fallback to neutral vector if no profile
            user_vector = [0.5] * 8
            confidence = 0.5
        else:
            user_vector = self._get_taste_vector(user_profile)
            confidence = float(user_profile.confidence_score)

        query = self.db.query(Dish).filter(Dish.is_available == True)
        if restaurant_id:
            query = query.filter(Dish.restaurant_id == restaurant_id)
        dishes = query.all()
        
        # Enforce hard constraints from intent
        if intent:
            filtered_dishes = []
            for dish in dishes:
                # Budget constraint
                if intent.budget and float(dish.price) > intent.budget:
                    continue
                # Allergen constraint
                if intent.allergens:
                    dish_allergens = [a.lower() for a in (dish.allergens or [])]
                    if any(a.lower() in dish_allergens for a in intent.allergens):
                        continue
                # Exclusions constraint
                if intent.excluded_ingredients:
                    dish_ingredients = [i.lower() for i in (dish.ingredients or [])]
                    if any(ex.lower() in dish_ingredients for ex in intent.excluded_ingredients):
                        continue
                filtered_dishes.append(dish)
            dishes = filtered_dishes
        
        recommendations = []
        for dish in dishes:
            dish_vector = self._get_taste_vector(dish)
            
            # 1. Taste Match (60%)
            taste_match = cosine_similarity(user_vector, dish_vector)
            
            # 2. Community Score (15%)
            community_score = self._get_community_score(user_id, dish.id, user_vector)
            
            # 3. Popularity / Restaurant Highlight (25%)
            popularity = float(dish.popularity_score)
            
            final_score = (taste_match * 0.60) + (community_score * 0.15) + (popularity * 0.25)
            
            # Generate reasons
            reasons = []
            if taste_match > 0.90:
                reasons.append(RecommendationReason(type="taste_match", text="Perfect match for your taste profile"))
            elif taste_match > 0.80:
                reasons.append(RecommendationReason(type="taste_match", text="Great match for your preferences"))
                
            if community_score > 0.70:
                reasons.append(RecommendationReason(type="community", text="People with similar taste loved this"))
                
            if popularity > 0.80:
                reasons.append(RecommendationReason(type="popularity", text="Highly popular dish"))
                
            if getattr(dish, 'chef_notes', None):
                reasons.append(RecommendationReason(type="chef", text="Chef's special highlight"))
                
            recommendations.append(
                DishRecommendation(
                    dish=DishOut.model_validate(dish),
                    score=final_score,
                    confidence=confidence,
                    reasons=reasons
                )
            )
            
        # Sort by score descending
        recommendations.sort(key=lambda x: x.score, reverse=True)
        
        return RecommendationResponse(user_id=user_id, recommendations=recommendations)

