from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant
from app.models.category import Category
from app.models.dish import Dish
from app.models.taste_profile import TasteProfile
from app.services.recommendation import RecommendationService
from app.services.rag.retrieval import RetrievalService
from app.services.rag.providers import SqliteVectorStoreProvider, GeminiEmbeddingProvider

class ContextBuilder:
    def __init__(self, db: Session):
        self.db = db
        
    def build_context(self, user_id: str, restaurant_id: str, page_context: str, selected_dish_id: str = None, query: str = None) -> Dict[str, Any]:
        """
        Gathers all necessary backend state to inject into the LLM prompt.
        """
        restaurant = self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        categories = self.db.query(Category).filter(Category.restaurant_id == restaurant_id).all()
        dishes = self.db.query(Dish).filter(Dish.restaurant_id == restaurant_id, Dish.is_available == True).all()
        
        user_profile = self.db.query(TasteProfile).filter(TasteProfile.user_id == user_id).first()
        
        rec_service = RecommendationService(self.db)
        recs_response = rec_service.get_recommendations(user_id, restaurant_id)
        
        # Format the menu
        menu_text = ""
        for cat in sorted(categories, key=lambda c: c.sort_order):
            menu_text += f"\n--- {cat.name} ---\n"
            cat_dishes = [d for d in dishes if d.category_id == cat.id]
            for d in sorted(cat_dishes, key=lambda d: d.display_order):
                menu_text += f"- {d.name} (₹{d.price}): {d.description} [ID: {d.id}]\n"
                
        # Format Top 5 Recommendations
        recs_text = "\n--- Top 5 Recommendations for User ---\n"
        for idx, rec in enumerate(recs_response.recommendations[:5]):
            recs_text += f"{idx+1}. {rec.dish.name} (Match: {int(rec.score * 100)}%) - Reasons: {', '.join(r.text for r in rec.reasons)}\n"
            
        # Format Taste Profile
        profile_text = "Taste Profile (0=Low, 1=High):\n"
        if user_profile:
            profile_text += f"Spice: {user_profile.spice_preference:.2f}\n"
            profile_text += f"Sweet: {user_profile.sweetness_preference:.2f}\n"
            profile_text += f"Creamy: {user_profile.creaminess_preference:.2f}\n"
            profile_text += f"Tangy: {user_profile.tanginess_preference:.2f}\n"
            profile_text += f"Masala Intensity: {user_profile.masala_intensity_preference:.2f}\n"
            profile_text += f"Crunchy: {user_profile.crunchiness_preference:.2f}\n"
            profile_text += f"Oiliness: {user_profile.oiliness_preference:.2f}\n"
            profile_text += f"Saltiness: {user_profile.saltiness_preference:.2f}\n"
        else:
            profile_text += "Unknown (No profile found)"
            
        selected_dish_info = ""
        if selected_dish_id:
            sd = next((d for d in dishes if d.id == selected_dish_id), None)
            if sd:
                selected_dish_info = f"\nUser is currently viewing dish: {sd.name} (ID: {sd.id})\n"
                
        retrieved_chunks = []
        if query:
            vector_store = SqliteVectorStoreProvider(self.db)
            embedding_provider = GeminiEmbeddingProvider()
            retrieval_service = RetrievalService(vector_store, embedding_provider)
            retrieval_result = retrieval_service.retrieve(query)
            retrieved_chunks = [chunk.model_dump() for chunk in retrieval_result.chunks]

        return {
            "restaurant_name": restaurant.name if restaurant else "Unknown",
            "menu_text": menu_text,
            "recommendations_text": recs_text,
            "profile_text": profile_text,
            "page_context": page_context,
            "selected_dish_info": selected_dish_info,
            "retrieved_chunks": retrieved_chunks
        }
