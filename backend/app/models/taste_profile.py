import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class TasteProfile(Base):
    __tablename__ = "taste_profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    # 0.0 to 1.0 vectors
    spice_preference = Column(Float, default=0.5)
    sweetness_preference = Column(Float, default=0.5)
    creaminess_preference = Column(Float, default=0.5)
    tanginess_preference = Column(Float, default=0.5)
    masala_intensity_preference = Column(Float, default=0.5)
    crunchiness_preference = Column(Float, default=0.5)
    oiliness_preference = Column(Float, default=0.5)
    saltiness_preference = Column(Float, default=0.5)
    
    confidence_score = Column(Float, default=0.0)
    onboarding_completed = Column(Boolean, default=False)
    
    from sqlalchemy.dialects.sqlite import JSON
    dna_matrix_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="taste_profile")
