from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RecommendationIntent(BaseModel):
    category: Optional[str] = None
    desired_taste: Optional[Dict[str, str]] = Field(default_factory=dict)
    dietary_restrictions: List[str] = Field(default_factory=list)
    budget: Optional[float] = None
    allergens: List[str] = Field(default_factory=list)
    excluded_ingredients: List[str] = Field(default_factory=list)
    sentiment: Optional[str] = None

class AssistantResult(BaseModel):
    intent: RecommendationIntent
    candidates: List[Dict[str, Any]] = Field(default_factory=list)
    ranked_result: List[Dict[str, Any]] = Field(default_factory=list)
    explanation: Optional[str] = None
