from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Uet application new
class ApplicationCreate(BaseModel):
    company_name: str
    job_role: str
    status: str = "Applied"
    notes: Optional[str] = None


# apdate application
class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    job_role: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None



class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    job_role: str
    status: str
    date_applied: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True