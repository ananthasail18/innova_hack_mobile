import pytest
from app.database.session import SessionLocal
from app.services.taste_dna_learning import TasteDNALearningService
from app.routes.taste_profile import record_taste_dna_feedback, FeedbackEventRequest
from app.models.taste_event import TasteEvent

def test_per_dish_feedback_persistence_and_idempotency():
    db = SessionLocal()
    try:
        user_id = "test_user_feedback"
        dish_id = "dish_123"
        idemp_key = "idemp_test_001"
        
        # First call should succeed and record it
        req = FeedbackEventRequest(
            user_id=user_id,
            dish_id=dish_id,
            feedback_type="thumbs_up",
            idempotency_key=idemp_key,
            event_type="POST_MEAL_FEEDBACK",
            dimension_deltas={"spice": 0.1},
            event_description="Test feedback"
        )
        
        result1 = record_taste_dna_feedback(request=req, db=db)
        assert result1["status"] == "success"
        assert "dna_matrix" in result1["data"]
        
        # Verify TasteEvent was saved
        event = db.query(TasteEvent).filter(TasteEvent.idempotency_key == idemp_key).first()
        assert event is not None
        assert event.dish_id == dish_id
        
        # Second call should be idempotent
        result2 = record_taste_dna_feedback(request=req, db=db)
        assert result2["status"] == "success"
        assert result2["message"] == "Already processed"
        
    finally:
        db.close()
