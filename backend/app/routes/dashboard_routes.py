from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.application import Application
from app.models.weak_area import WeakArea
from app.schemas.weak_area_schema import WeakAreaResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# GET 
@router.get("/{user_id}")
def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    all_apps = db.query(Application).filter(Application.user_id == user_id).all()

    total = len(all_apps)
    applied = sum(1 for a in all_apps if a.status == "Applied")
    interview_scheduled = sum(1 for a in all_apps if a.status == "Interview Scheduled")
    rejected = sum(1 for a in all_apps if a.status == "Rejected")
    selected = sum(1 for a in all_apps if a.status == "Selected/Offer")

   # succes rate formmula
    success_rate = round((selected / total) * 100, 1) if total > 0 else 0

    return {
        "total_applications": total,
        "applied": applied,
        "interview_scheduled": interview_scheduled,
        "rejected": rejected,
        "selected": selected,
        "success_rate": success_rate
    }



@router.get("/weaknesses/{user_id}", response_model=List[WeakAreaResponse])
def get_weaknesses(user_id: int, db: Session = Depends(get_db)):
    
    app_ids = [
        a.id for a in db.query(Application).filter(Application.user_id == user_id).all()
    ]

    if not app_ids:
        return []

    
    weak_areas = db.query(WeakArea).filter(WeakArea.application_id.in_(app_ids)).all()
    return weak_areas
