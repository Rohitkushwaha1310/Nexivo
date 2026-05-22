from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WeakAreaResponse(BaseModel):
    id: int
    application_id: int
    topic: str
    detected_from: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True