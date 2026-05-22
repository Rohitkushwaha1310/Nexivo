from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.application import Application
from app.schemas.application_schema import ApplicationCreate, ApplicationUpdate, ApplicationResponse

router = APIRouter(prefix="/applications", tags=["Applications"])


#new application
@router.post("/{user_id}", response_model=ApplicationResponse)
def create_application(user_id: int, app_data: ApplicationCreate, db: Session = Depends(get_db)):
    new_app = Application(
        user_id=user_id,
        company_name=app_data.company_name,
        job_role=app_data.job_role,
        status=app_data.status,
        notes=app_data.notes
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app


# Get application

@router.get("/user/{user_id}", response_model=List[ApplicationResponse])
def get_all_applications(user_id: int, db: Session = Depends(get_db)):
    applications = db.query(Application).filter(Application.user_id == user_id).all()
    return applications



@router.get("/{app_id}", response_model=ApplicationResponse)
def get_application(app_id: int, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


# put app
@router.put("/{app_id}", response_model=ApplicationResponse)
def update_application(app_id: int, app_data: ApplicationUpdate, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    # update
    if app_data.company_name is not None:
        app.company_name = app_data.company_name
    if app_data.job_role is not None:
        app.job_role = app_data.job_role
    if app_data.status is not None:
        app.status = app_data.status
    if app_data.notes is not None:
        app.notes = app_data.notes

    db.commit()
    db.refresh(app)
    return app


#dlt app
@router.delete("/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app)
    db.commit()
    return {"message": "Application deleted successfully"}
