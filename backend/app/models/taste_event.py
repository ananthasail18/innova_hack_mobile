import uuid
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship
from app.database.base import Base

class TasteEvent(Base):
    __tablename__ = "taste_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    dish_id = Column(String, ForeignKey("dishes.id"), nullable=False, index=True)
    feedback_type = Column(String, nullable=False)
    idempotency_key = Column(String, unique=True, index=True, nullable=False)
    
    profile_before = Column(JSON, nullable=True)
    profile_after = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="taste_events")
    dish = relationship("Dish")
