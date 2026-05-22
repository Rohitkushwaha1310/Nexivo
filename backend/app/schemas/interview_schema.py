from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# new interviw
class InterviewRoundCreate(BaseModel):
    round_name: str
    feedback: Optional[str] = None
    result: str = "Pending"


class InterviewRoundUpdate(BaseModel):
    round_name: Optional[str] = None
    feedback: Optional[str] = None
    result: Optional[str] = None



class InterviewRoundResponse(BaseModel):
    id: int
    application_id: int
    round_name: str
    feedback: Optional[str]
    result: str
    interview_date: datetime

    class Config:
        from_attributes = True