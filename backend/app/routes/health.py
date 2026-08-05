from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.middleware.responses import success_response, ResponseEnvelope
from app.database.session import get_db
from app.models.dish import Dish
from app.models.restaurant import Restaurant

router = APIRouter()

@router.get("/health", response_model=ResponseEnvelope)
def health_check():
    return success_response(data={"status": "ok"}, message="System is healthy")

@router.get("/health/live", response_model=ResponseEnvelope)
def health_live():
    return success_response(data={"status": "alive"}, message="System is live")

@router.get("/health/ready", response_model=ResponseEnvelope)
def health_ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        restaurant_count = db.query(Restaurant).count()
        dish_count = db.query(Dish).count()
        
        if restaurant_count == 0 or dish_count == 0:
            raise Exception("Database is empty or not seeded")
            
        return success_response(data={"status": "ready"}, message="System is ready")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
