from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TasteProfileBase(BaseModel):
    spice_preference: float = Field(0.5, ge=0.0, le=1.0)
    sweetness_preference: float = Field(0.5, ge=0.0, le=1.0)
    creaminess_preference: float = Field(0.5, ge=0.0, le=1.0)
    tanginess_preference: float = Field(0.5, ge=0.0, le=1.0)
    masala_intensity_preference: float = Field(0.5, ge=0.0, le=1.0)
    crunchiness_preference: float = Field(0.5, ge=0.0, le=1.0)
    oiliness_preference: float = Field(0.5, ge=0.0, le=1.0)
    saltiness_preference: float = Field(0.5, ge=0.0, le=1.0)

class TasteProfileCreate(TasteProfileBase):
    user_id: str

class TasteProfileOut(TasteProfileBase):
    id: str
    user_id: str
    confidence_score: float = Field(0.0, ge=0.0, le=1.0)
    onboarding_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class QuizAnswer(BaseModel):
    question_id: str
    selected_option_id: str

class QuizSubmission(BaseModel):
    user_id: str
    answers: List[QuizAnswer]
