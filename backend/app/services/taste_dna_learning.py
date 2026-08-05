import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.taste_profile import TasteProfile
from app.schemas.taste_dna import TasteDNAMatrix, TasteDNADimensionDetail, DimensionContributions
from app.schemas.taste_profile import QuizSubmission
from app.services.taste_identity import TasteIdentityService

logger = logging.getLogger(__name__)

# Configurable Learning Weights
LEARNING_WEIGHTS = {
    "QUIZ": 0.35,
    "ORDER_COMPLETED": 0.10,
    "POST_MEAL_FEEDBACK": 0.25,
    "REPEATED_POSITIVE_ORDERS": 0.25,
    "REPEATED_REORDERS": 0.40,
    "RECOMMENDATION_FEEDBACK": 0.20
}

DIMENSION_MAP = {
    "spice": "spice_preference",
    "sweetness": "sweetness_preference",
    "creaminess": "creaminess_preference",
    "tanginess": "tanginess_preference",
    "masala_intensity": "masala_intensity_preference",
    "crunchiness": "crunchiness_preference",
    "oiliness": "oiliness_preference",
    "saltiness": "saltiness_preference"
}

class TasteDNALearningService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_dna(self, user_id: str) -> TasteProfile:
        profile = self.db.query(TasteProfile).filter(TasteProfile.user_id == user_id).first()
        if not profile:
            profile = TasteProfile(
                user_id=user_id,
                spice_preference=0.5,
                sweetness_preference=0.5,
                creaminess_preference=0.5,
                tanginess_preference=0.5,
                masala_intensity_preference=0.5,
                crunchiness_preference=0.5,
                oiliness_preference=0.5,
                saltiness_preference=0.5,
                confidence_score=0.55,
                onboarding_completed=False,
                dna_matrix_json=self._build_default_matrix(0.5, 0.55).model_dump()
            )
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
        elif not profile.dna_matrix_json:
            profile.dna_matrix_json = self._build_matrix_from_profile(profile).model_dump()
            self.db.commit()
            self.db.refresh(profile)
            
        return profile

    def initialize_from_quiz(self, submission: QuizSubmission) -> TasteProfile:
        user_id = submission.user_id
        profile_create = TasteIdentityService.generate_profile(submission)
        
        answered_count = len(submission.answers)
        initial_confidence = round(min(0.60, max(0.50, 0.50 + (answered_count * 0.015))), 2)
        today = datetime.utcnow().strftime("%Y-%m-%d")

        matrix_dict = {}
        for dim_key, pref_key in DIMENSION_MAP.items():
            val = getattr(profile_create, pref_key, 0.5)
            matrix_dict[dim_key] = TasteDNADimensionDetail(
                value=round(val, 2),
                confidence=initial_confidence,
                last_updated=today,
                sources=["Onboarding Quiz"],
                contributions=DimensionContributions(quiz=1.0, feedback=0.0, orders=0.0, recommendations=0.0)
            )
            
        matrix = TasteDNAMatrix(
            spice=matrix_dict["spice"],
            sweetness=matrix_dict["sweetness"],
            creaminess=matrix_dict["creaminess"],
            tanginess=matrix_dict["tanginess"],
            masala_intensity=matrix_dict["masala_intensity"],
            crunchiness=matrix_dict["crunchiness"],
            oiliness=matrix_dict["oiliness"],
            saltiness=matrix_dict["saltiness"],
            overall_confidence=initial_confidence,
            completion_percentage=100.0,
            recent_evolution=[
                {
                    "date": today,
                    "event": "Taste DNA Created",
                    "description": f"Initial Taste DNA established from onboarding quiz with {int(initial_confidence*100)}% confidence.",
                    "source": "Onboarding Quiz"
                }
            ]
        )

        db_profile = self.db.query(TasteProfile).filter(TasteProfile.user_id == user_id).first()
        if not db_profile:
            db_profile = TasteProfile(user_id=user_id)
            self.db.add(db_profile)

        for dim_key, pref_key in DIMENSION_MAP.items():
            setattr(db_profile, pref_key, getattr(profile_create, pref_key))

        db_profile.confidence_score = initial_confidence
        db_profile.onboarding_completed = True
        db_profile.dna_matrix_json = matrix.model_dump()

        self.db.commit()
        self.db.refresh(db_profile)
        logger.info(f"Initialized Taste DNA for user {user_id} with confidence {initial_confidence}")
        
        self.recalibrate_community_signals(user_id)
        return db_profile

    def record_feedback_event(
        self,
        user_id: str,
        event_type: str,
        dimension_deltas: Dict[str, float],
        event_description: str,
        commit: bool = True
    ) -> TasteProfile:
        """
        Gradual learning engine:
        Applies soft lerp updates to Taste DNA dimensions so single meals don't cause drastic jumps.
        """
        profile = self.get_or_create_dna(user_id)
        matrix = TasteDNAMatrix(**profile.dna_matrix_json)
        
        # Synchronize matrix values with flat DB columns if out-of-sync (e.g. from seed files)
        for dim, pref_col in DIMENSION_MAP.items():
            db_val = getattr(profile, pref_col)
            if db_val is not None:
                matrix_dim = getattr(matrix, dim)
                if abs(matrix_dim.value - db_val) > 0.001:
                    matrix_dim.value = db_val
        
        weight = LEARNING_WEIGHTS.get(event_type, 0.20)
        alpha = round(weight * 0.25, 3)  # Smoothing factor (e.g. 0.06 - 0.10)
        today = datetime.utcnow().strftime("%Y-%m-%d")

        source_label = event_type.replace("_", " ").title()
        evolution_changes = []

        for dim_key, delta in dimension_deltas.items():
            if dim_key not in DIMENSION_MAP:
                continue
                
            dim_detail: TasteDNADimensionDetail = getattr(matrix, dim_key)
            old_val = dim_detail.value
            
            # Target value towards which we lerp
            target_val = max(0.0, min(1.0, old_val + delta))
            new_val = round(old_val + alpha * (target_val - old_val), 2)
            
            # Monotonically increase confidence
            new_confidence = round(min(0.98, dim_detail.confidence + (weight * 0.04)), 2)
            
            # Update sources if new
            sources = dim_detail.sources
            if source_label not in sources:
                sources.append(source_label)

            # Rebalance contributions
            contribs = dim_detail.contributions
            if "FEEDBACK" in event_type:
                contribs.feedback = round(min(0.60, contribs.feedback + 0.10), 2)
                contribs.quiz = round(max(0.10, 1.0 - contribs.feedback - contribs.orders - contribs.recommendations), 2)
            elif "ORDER" in event_type or "REORDER" in event_type:
                contribs.orders = round(min(0.60, contribs.orders + 0.10), 2)
                contribs.quiz = round(max(0.10, 1.0 - contribs.feedback - contribs.orders - contribs.recommendations), 2)
            elif "RECOMMENDATION" in event_type:
                contribs.recommendations = round(min(0.50, contribs.recommendations + 0.10), 2)
                contribs.quiz = round(max(0.10, 1.0 - contribs.feedback - contribs.orders - contribs.recommendations), 2)

            dim_detail.value = new_val
            dim_detail.confidence = new_confidence
            dim_detail.last_updated = today
            dim_detail.sources = sources
            dim_detail.contributions = contribs
            
            # Apply to flat DB column for fast SQL vector ops
            setattr(profile, DIMENSION_MAP[dim_key], new_val)
            evolution_changes.append(f"{dim_key.replace('_', ' ').title()} adjusted {old_val:.2f} ➔ {new_val:.2f}")

        # Update overall profile confidence
        all_confidences = [getattr(matrix, d).confidence for d in DIMENSION_MAP.keys()]
        matrix.overall_confidence = round(sum(all_confidences) / len(all_confidences), 2)
        profile.confidence_score = matrix.overall_confidence

        # Append to recent evolution timeline
        matrix.recent_evolution.insert(0, {
            "date": today,
            "event": event_description,
            "description": f"{', '.join(evolution_changes)} (Confidence: {int(matrix.overall_confidence*100)}%).",
            "source": source_label
        })
        matrix.recent_evolution = matrix.recent_evolution[:10]  # keep top 10 timeline entries

        profile.dna_matrix_json = matrix.model_dump()
        if commit:
            self.db.commit()
            self.db.refresh(profile)
        else:
            self.db.flush()

        self.recalibrate_community_signals(user_id)
        return profile

    def recalibrate_community_signals(self, user_id: str):
        """Triggers community recalibration when Taste DNA changes"""
        logger.info(f"Recalibrating community signals for user {user_id}")

    def _build_default_matrix(self, default_val: float, default_conf: float) -> TasteDNAMatrix:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        details = {}
        for dim_key in DIMENSION_MAP.keys():
            details[dim_key] = TasteDNADimensionDetail(
                value=default_val,
                confidence=default_conf,
                last_updated=today,
                sources=["Default Profile"],
                contributions=DimensionContributions(quiz=1.0, feedback=0.0, orders=0.0, recommendations=0.0)
            )
        return TasteDNAMatrix(
            spice=details["spice"],
            sweetness=details["sweetness"],
            creaminess=details["creaminess"],
            tanginess=details["tanginess"],
            masala_intensity=details["masala_intensity"],
            crunchiness=details["crunchiness"],
            oiliness=details["oiliness"],
            saltiness=details["saltiness"],
            overall_confidence=default_conf,
            completion_percentage=100.0,
            recent_evolution=[]
        )

    def _build_matrix_from_profile(self, profile: TasteProfile) -> TasteDNAMatrix:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        conf = float(profile.confidence_score or 0.55)
        details = {}
        for dim_key, pref_key in DIMENSION_MAP.items():
            val = float(getattr(profile, pref_key, 0.5))
            details[dim_key] = TasteDNADimensionDetail(
                value=val,
                confidence=conf,
                last_updated=today,
                sources=["Onboarding Quiz"],
                contributions=DimensionContributions(quiz=0.8, feedback=0.1, orders=0.1, recommendations=0.0)
            )
        return TasteDNAMatrix(
            spice=details["spice"],
            sweetness=details["sweetness"],
            creaminess=details["creaminess"],
            tanginess=details["tanginess"],
            masala_intensity=details["masala_intensity"],
            crunchiness=details["crunchiness"],
            oiliness=details["oiliness"],
            saltiness=details["saltiness"],
            overall_confidence=conf,
            completion_percentage=100.0,
            recent_evolution=[
                {
                    "date": today,
                    "event": "Taste DNA Synchronized",
                    "description": "Established baseline Taste DNA matrix.",
                    "source": "System Sync"
                }
            ]
        )
