import uuid
from sqlalchemy import Column, String, DateTime, func, ForeignKey, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship
from app.database.base import Base

class RecommendationDecision(Base):
    __tablename__ = "recommendation_decisions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    original_request = Column(Text, nullable=False)
    
    parsed_intent = Column(JSON, nullable=True)
    candidates = Column(JSON, nullable=True)
    ranked_result = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="recommendation_decisions")
