import os
import sys

from app.database.session import SessionLocal
from app.models.user import User
from app.models.taste_profile import TasteProfile

def seed_ananth():
    db = SessionLocal()
    
    # Check if Ananth exists
    user = db.query(User).filter((User.name.ilike('%ananth%')) | (User.email.ilike('%ananth%'))).first()
    
    if not user:
        user = User(name="Ananth", email="ananth@taste.ai")
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created user Ananth with ID: {user.id}")
    else:
        print(f"User Ananth already exists with ID: {user.id}")
        
    # Check if TasteProfile exists
    profile = db.query(TasteProfile).filter(TasteProfile.user_id == user.id).first()
    
    if not profile:
        profile = TasteProfile(
            user_id=user.id,
            spice_preference=0.85,      # High spice
            sweetness_preference=0.30,  # Low sweet
            creaminess_preference=0.40, 
            tanginess_preference=0.70,  # High tangy
            masala_intensity_preference=0.60,
            crunchiness_preference=0.80,     # Loves crunch
            oiliness_preference=0.90,       # Very oily/rich
            saltiness_preference=0.60
        )
        db.add(profile)
        db.commit()
        print("Created a real Taste DNA profile for Ananth!")
    else:
        # Update existing
        profile.spice_preference = 0.85
        profile.sweetness_preference = 0.30
        profile.creaminess_preference = 0.40
        profile.tanginess_preference = 0.70
        profile.masala_intensity_preference = 0.60
        profile.crunchiness_preference = 0.80
        profile.oiliness_preference = 0.90
        profile.saltiness_preference = 0.60
        profile.dna_matrix_json = None
        db.commit()
        print("Updated existing Taste DNA profile for Ananth with real data!")

if __name__ == "__main__":
    seed_ananth()
